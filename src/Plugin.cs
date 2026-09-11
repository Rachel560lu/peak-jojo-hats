using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using MoreCustomizations;
using MoreCustomizations.Data;
using UnityEngine;
using Object = UnityEngine.Object;

namespace JojoHats;

[BepInPlugin("midor.peak.jojohats", "JOJO Scout Hats", Version)]
[BepInDependency("MoreCustomizations", "1.1.10")]
public sealed class Plugin : BaseUnityPlugin
{
    internal const string Version = "0.5.2";
    private const string Prefix = "jojo_mvp_";
    private static readonly string[] Ids = {
        "01_jotaro_cap", "02_josuke_pompadour", "03_giorno_rolls",
        "04_jonathan_hair", "05_jolyne_buns", "06_joseph_hair"
    };
    private readonly List<Object> ownedAssets = new();
    private readonly List<CustomHat_V1> hats = new();
    private GameObject? templates;
    private IReadOnlyDictionary<Customization.Type, IReadOnlyList<CustomizationData>>? originalCatalog;
    private string contentFingerprint = "";
    private bool catalogPublished;

    private void Awake()
    {
        try
        {
            string root = Path.Combine(Path.GetDirectoryName(Info.Location)!, "assets");
            var previous = MoreCustomizationsPlugin.AllCustomizationsData
                ?? throw new InvalidOperationException("More Customizations did not initialize. Reinstall the official More Customizations dependency in your mod-manager profile and keep its built-in.pcab. Do not run the old JOJO-only patch script. No other cosmetics or files were changed.");
            originalCatalog = previous;
            // Prepare everything before touching the shared catalog: a missing model never
            // results in different subsets/indices silently loading on different clients.
            Texture2D atlas = LoadTexture(Path.Combine(root, "palette.png"));
            atlas.filterMode = FilterMode.Point;
            templates = new GameObject("JOJO Hat Templates");
            templates.SetActive(false);
            Object.DontDestroyOnLoad(templates);
            foreach (string id in Ids)
            {
                string folder = Path.Combine(root, id);
                MeshData data = JsonUtility.FromJson<MeshData>(File.ReadAllText(Path.Combine(folder, "mesh.json")));
                Validate(data, id);
                Mesh mesh = MakeMesh(data);
                Texture2D main = atlas;
                if (!string.IsNullOrEmpty(data.texture))
                {
                    main = LoadTexture(Path.Combine(folder, data.texture));
                    main.filterMode = FilterMode.Bilinear;
                }
                var prefab = new GameObject(Prefix + id);
                prefab.transform.SetParent(templates.transform, false);
                prefab.AddComponent<MeshFilter>().sharedMesh = mesh;
                prefab.AddComponent<MeshRenderer>();
                // activeSelf stays true; only the template container is inactive.
                // Framework clones these into the head slot and controls their visibility.
                var hat = ScriptableObject.CreateInstance<CustomHat_V1>();
                ownedAssets.Add(hat);
                hat.name = Prefix + id;
                Set(hat, nameof(CustomHat_V1.Icon), LoadTexture(Path.Combine(folder, "icon.png")));
                Set(hat, nameof(CustomHat_V1.Prefab), prefab);
                Set(hat, nameof(CustomHat_V1.MainTexture), main);
                Set(hat, nameof(CustomHat_V1.SubTexture), main);
                Set(hat, nameof(CustomHat_V1.PositionOffset), Vector3.zero);
                Set(hat, nameof(CustomHat_V1.EulerAngleOffset), Vector3.zero);
                if (!hat.IsValid) throw new InvalidDataException("Hat validation failed: " + id);
                hats.Add(hat);
                Logger.LogInfo($"Prepared {id}: {mesh.vertexCount} vertices, {data.triangles.Length / 3} triangles");
            }
            // Preserve every existing entry/index. Only append our stable, namespaced IDs.
            // No category clearing, global sorting, save rewriting or dependency file changes.
            var next = CatalogMerge.Append(previous, Customization.Type.Hat,
                hats.Cast<CustomizationData>().ToArray(), item => item.name);
            contentFingerprint = Fingerprint(root);
            // 1.1.10 has no public RegisterHat API. Isolate the private setter bridge here.
            SetStatic(typeof(MoreCustomizationsPlugin), "AllCustomizationsData", next);
            catalogPublished = true;
            int existingHats = previous.TryGetValue(Customization.Type.Hat, out var entries) ? entries.Count : 0;
            Logger.LogInfo($"JOJO_REGISTERED=6; mode=append; existingHats={existingHats}; totalHats={next[Customization.Type.Hat].Count}; contentSHA256={contentFingerprint}");
            Logger.LogInfo("Other cosmetics preserved. For multiplayer, every player needs the same complete cosmetic profile and versions; mesh files are not sent over the network.");
            if (Environment.GetCommandLineArgs().Contains("--jojo-smoke-test"))
            {
                File.WriteAllLines(Path.Combine(Paths.BepInExRootPath, "jojo-smoke.txt"), new[] { "version=" + Version, "result=PENDING" });
                StartCoroutine(SmokeTest());
            }
        }
        catch (Exception e)
        {
            Logger.LogError((catalogPublished ? "JOJO post-registration diagnostic failed: " : "JOJO initialization aborted; other cosmetics left unchanged: ") + e);
            // Once published, other objects may reference our assets; never destroy them here.
            if (!catalogPublished)
            {
                if (templates) Object.Destroy(templates);
                foreach (Object asset in ownedAssets) if (asset) Object.Destroy(asset);
                enabled = false;
            }
            if (Environment.GetCommandLineArgs().Contains("--jojo-smoke-test"))
            {
                File.WriteAllLines(Path.Combine(Paths.BepInExRootPath, "jojo-smoke.txt"), new[] { "version=" + Version, "result=FAIL: " + e });
                if (Environment.GetCommandLineArgs().Contains("--jojo-test-quit")) Application.Quit();
            }
        }
    }

    private static string Fingerprint(string root)
    {
        // Hash only our shipped content, never player data, absolute paths or other mods.
        using var hash = SHA256.Create();
        var records = new List<string>();
        foreach (string relative in new[] { "palette.png" }.Concat(Ids.SelectMany(id =>
                     new[] { id + "/mesh.json", id + "/icon.png" })))
            records.Add(relative + ":" + BitConverter.ToString(hash.ComputeHash(File.ReadAllBytes(Path.Combine(root, relative)))).Replace("-", ""));
        return BitConverter.ToString(hash.ComputeHash(Encoding.UTF8.GetBytes(string.Join("\n", records)))).Replace("-", "").ToLowerInvariant();
    }

    private Texture2D LoadTexture(string path)
    {
        var texture = new Texture2D(2, 2, TextureFormat.RGBA32, false);
        ownedAssets.Add(texture);
        if (!ImageConversion.LoadImage(texture, File.ReadAllBytes(path)))
            throw new InvalidDataException("Cannot decode " + path);
        texture.name = Path.GetFileName(path);
        texture.wrapMode = TextureWrapMode.Clamp;
        return texture;
    }

    private Mesh MakeMesh(MeshData data)
    {
        int count = data.positions.Length / 3;
        var vertices = new Vector3[count];
        var uv = new Vector2[count];
        var colors = new Color[count];
        for (int i = 0; i < count; i++)
        {
            vertices[i] = new Vector3(data.positions[i*3], data.positions[i*3+1], data.positions[i*3+2]);
            uv[i] = new Vector2(data.uv[i*2], data.uv[i*2+1]);
            colors[i] = Color.white;
        }
        var mesh = new Mesh { name = Prefix + data.name };
        ownedAssets.Add(mesh);
        mesh.vertices = vertices;
        mesh.uv = uv;
        mesh.colors = colors;
        // Framework assigns exactly two materials. Keep a matching empty secondary submesh.
        mesh.subMeshCount = 2;
        mesh.SetTriangles(data.triangles, 0);
        mesh.SetTriangles(Array.Empty<int>(), 1);
        if (data.normals != null && data.normals.Length == count * 3)
        {
            var normals = new Vector3[count];
            for (int i = 0; i < count; i++) normals[i] = new Vector3(data.normals[i*3], data.normals[i*3+1], data.normals[i*3+2]);
            mesh.normals = normals;
        }
        else mesh.RecalculateNormals(); // Compatibility with legacy assets.
        mesh.RecalculateBounds();
        return mesh;
    }

    internal static void Validate(MeshData data, string expected)
    {
        if (data == null || data.name != expected || data.positions == null || data.triangles == null || data.uv == null)
            throw new InvalidDataException("Missing or mismatched mesh: " + expected);
        int n = data.positions.Length / 3;
        if (!string.IsNullOrEmpty(data.texture) && data.texture != "albedo.png")
            throw new InvalidDataException("Unsupported texture path: " + expected);
        if (data.normals != null && data.normals.Length != 0)
        {
            if (data.normals.Length != data.positions.Length || data.normals.Any(x => float.IsNaN(x) || float.IsInfinity(x)))
                throw new InvalidDataException("Invalid normal data: " + expected);
            for (int i = 0; i < data.normals.Length; i += 3)
            {
                float squared = data.normals[i]*data.normals[i] + data.normals[i+1]*data.normals[i+1] + data.normals[i+2]*data.normals[i+2];
                if (squared < .98f || squared > 1.02f) throw new InvalidDataException("Non-unit normal: " + expected);
            }
        }
        if (n == 0 || n > 65000 || data.positions.Length % 3 != 0 || data.uv.Length != n*2 || data.triangles.Length == 0 || data.triangles.Length % 3 != 0)
            throw new InvalidDataException("Invalid mesh dimensions: " + expected);
        if (data.positions.Any(x => float.IsNaN(x) || float.IsInfinity(x) || Math.Abs(x) > 8) ||
            data.uv.Any(x => float.IsNaN(x) || float.IsInfinity(x) || x < 0 || x > 1) ||
            data.triangles.Any(i => i < 0 || i >= n))
            throw new InvalidDataException("Invalid mesh coordinates or indices: " + expected);
    }

    private static void Set(object target, string name, object value)
    {
        PropertyInfo property = target.GetType().GetProperty(name, BindingFlags.Instance | BindingFlags.Public)
            ?? throw new MissingMemberException(target.GetType().FullName, name);
        (property.GetSetMethod(true) ?? throw new MissingMethodException(name)).Invoke(target, new[] { value });
    }
    private static void SetStatic(Type type, string name, object value)
    {
        PropertyInfo property = type.GetProperty(name, BindingFlags.Static | BindingFlags.Public)
            ?? throw new MissingMemberException(type.FullName, name);
        (property.GetSetMethod(true) ?? throw new MissingMethodException(name)).Invoke(null, new[] { value });
    }

    private IEnumerator SmokeTest()
    {
        // Explicit test launch only. Verify in the real Unity process, without touching save selections.
        yield return new WaitForSecondsRealtime(18);
        var results = new List<string> { "version=" + Version, "registered=" + hats.Count, "contentSHA256=" + contentFingerprint };
        var catalog = MoreCustomizationsPlugin.AllCustomizationsData;
        int other = catalog.Where(p => p.Key != Customization.Type.Hat).Sum(p => p.Value.Count);
        results.Add("customNonHatEntries=" + other);
        results.Add("customHatEntries=" + catalog[Customization.Type.Hat].Count);
        results.Add("pcabFiles=" + Directory.GetFiles(Paths.PluginPath, "*.pcab", SearchOption.AllDirectories).Length);
        try
        {
        foreach (var h in hats)
        {
            var clone = Object.Instantiate(h.Prefab);
            clone.SetActive(true);
            var renderer = clone.GetComponent<MeshRenderer>();
            var mesh = clone.GetComponent<MeshFilter>().sharedMesh;
            bool paletteOk = h.MainTexture == hats[0].MainTexture && h.MainTexture.height == 16 && h.MainTexture.filterMode == FilterMode.Point;
            bool normalsOk = mesh.normals.Length == mesh.vertexCount;
            results.Add(h.name + ": active=" + clone.activeSelf + ", vertices=" + mesh.vertexCount + ", renderer=" + (renderer != null));
            Object.Destroy(clone);
            if (!paletteOk || !normalsOk) throw new InvalidOperationException("Shared palette/normal assertion failed: " + h.name);
        }
        Shader shader = Shader.Find("W/Character");
        results.Add("characterShader=" + (shader != null));
        results.Add("runtime=" + Application.unityVersion);
            if (!shader) throw new InvalidOperationException("Game character shader missing.");
            VerifyPreservedCatalog(catalog);
            var twice = CatalogMerge.Append(catalog, Customization.Type.Hat,
                hats.Cast<CustomizationData>().ToArray(), item => item.name);
            if (twice[Customization.Type.Hat].Count != catalog[Customization.Type.Hat].Count)
                throw new InvalidOperationException("Duplicate registration changed the catalog.");
            results.Add("existingCatalogPreserved=PASS; duplicateRegistration=PASS");
            IntegrationSmoke(results);
            results.Add("result=PASS");
        }
        catch (Exception ex)
        {
            results.Add("result=FAIL: " + ex);
            Logger.LogError("JOJO integration check: " + ex);
        }
        File.WriteAllLines(Path.Combine(Paths.BepInExRootPath, "jojo-smoke.txt"), results);
        Logger.LogInfo("JOJO_SMOKE_FINISHED: " + results.Last());
        if (Environment.GetCommandLineArgs().Contains("--jojo-test-quit")) Application.Quit();
    }

    private void VerifyPreservedCatalog(IReadOnlyDictionary<Customization.Type, IReadOnlyList<CustomizationData>> actual)
    {
        if (originalCatalog == null) throw new InvalidOperationException("Missing pre-registration snapshot.");
        foreach (var category in originalCatalog)
        {
            if (!actual.TryGetValue(category.Key, out var entries) || entries.Count < category.Value.Count)
                throw new InvalidOperationException("Existing category removed or shortened: " + category.Key);
            for (int i = 0; i < category.Value.Count; i++)
                if (!ReferenceEquals(entries[i], category.Value[i]))
                    throw new InvalidOperationException("Existing cosmetic changed index: " + category.Key + "/" + i);
            if (category.Key != Customization.Type.Hat && entries.Count != category.Value.Count)
                throw new InvalidOperationException("Unrelated cosmetic category changed.");
        }
        foreach (string id in Ids)
            if (actual[Customization.Type.Hat].Count(item => item.name == Prefix + id) != 1)
                throw new InvalidOperationException("Missing or duplicate JOJO hat: " + id);
    }

    private void IntegrationSmoke(List<string> results)
    {
        GameObject source = Resources.Load<GameObject>("Character");
        if (!source) throw new InvalidOperationException("Game Character prefab not found.");
        Type patch = typeof(MoreCustomizationsPlugin).Assembly.GetType("MoreCustomizations.Patches.CharacterCustomizationPatch", true);
        Type passportPatch = typeof(MoreCustomizationsPlugin).Assembly.GetType("MoreCustomizations.Patches.PassportManagerPatch", true);
        FieldInfo shaderCache = patch.GetField("_characterShader", BindingFlags.NonPublic | BindingFlags.Static)
            ?? throw new MissingFieldException(patch.FullName, "_characterShader");
        FieldInfo materialCache = passportPatch.GetField("materialTemplate", BindingFlags.NonPublic | BindingFlags.Static)
            ?? throw new MissingFieldException(passportPatch.FullName, "materialTemplate");
        object? savedShader = shaderCache.GetValue(null);
        object? savedMaterialTemplate = materialCache.GetValue(null);
        var originalMaterials = new HashSet<int>(Resources.FindObjectsOfTypeAll<Material>().Select(material => material.GetInstanceID()));
        HashSet<int>? optionsBeforePassport = null;
        // Clone inactive: do not run gameplay/network Awake, create a player, or alter saves.
        GameObject test = Object.Instantiate(source, templates!.transform, false);
        GameObject? passportTest = null;
        int savedBaseHatCount = MoreCustomizationsPlugin.BaseHatCount;
        int savedOverrideHatCount = MoreCustomizationsPlugin.OverrideHatCount;
        try
        {
        test.name = "JOJO isolated prefab integration";
        var cc = test.GetComponent<CharacterCustomization>();
        if (!cc || !cc.refs) throw new InvalidOperationException("CharacterCustomization refs missing.");
        int original = cc.refs.playerHats.Length;
        patch.GetMethod("Awake", BindingFlags.Static | BindingFlags.NonPublic)!.Invoke(null, new object[] { cc });
        Renderer[] ours = cc.refs.playerHats.Where(r => r && r.name.StartsWith(Prefix, StringComparison.Ordinal)).ToArray();
        if (ours.Length != 6) throw new InvalidOperationException("Not all six hats attached to actual Character prefab.");
        int customHats = MoreCustomizationsPlugin.AllCustomizationsData[Customization.Type.Hat].Count;
        if (cc.refs.playerHats.Length < original + customHats) throw new InvalidOperationException("Existing custom hat renderers missing.");
        results.Add($"actualCharacterPrefab: baseRenderers={original}; jojoRenderers={ours.Length}");
        foreach (Renderer renderer in ours)
        {
            Mesh actualMesh = renderer.GetComponent<MeshFilter>().sharedMesh;
            if (actualMesh.normals.Length != actualMesh.vertexCount || actualMesh.normals.Any(n => n.sqrMagnitude < .98f || n.sqrMagnitude > 1.02f))
                throw new InvalidOperationException("Missing or invalid authored normals: " + renderer.name);
            if (renderer.sharedMaterials.Any(m => !m || m.shader != Shader.Find("W/Character")))
                throw new InvalidOperationException("Wrong renderer shader: " + renderer.name);
            results.Add(renderer.name + ": headLocalPosition=" + renderer.transform.localPosition + "; rotation=" + renderer.transform.localEulerAngles);
            results.Add(renderer.name + ": authoredNormals=" + actualMesh.normals.Length);
        }
        results.Add("headTransform=" + cc.refs.hatTransform);
        results.Add("bodyTransform=" + cc.refs.mainRenderer.transform.position + "; scale=" + cc.refs.mainRenderer.transform.lossyScale);
        foreach (Renderer baseHat in cc.refs.playerHats.Take(8))
            if (baseHat) results.Add("baseHat=" + baseHat.name + "; local=" + baseHat.transform.localPosition + "; world=" + baseHat.transform.position);
        if (Environment.GetCommandLineArgs().Contains("--jojo-network-index-test"))
            NetworkIndexSmoke.Verify(results, Array.FindIndex(cc.refs.playerHats,
                renderer => renderer && renderer.name == Prefix + Ids[0]));
        else
            results.Add("localGameSerializationRoundTrip=NOT_RUN; requires real initialized passport; twoClientMultiplayer=NOT_TESTED");
        // Exercise the framework's passport registration against an isolated empty catalog.
        // This checks icon/type/name registration, not interactive passport UI navigation.
        passportTest = new GameObject("JOJO isolated passport registration");
        passportTest.transform.SetParent(templates.transform, false);
        object customization = passportTest.AddComponent(typeof(Customization));
        foreach (FieldInfo field in typeof(Customization).GetFields(BindingFlags.Public | BindingFlags.Instance))
            if (field.FieldType == typeof(CustomizationOption[])) field.SetValue(customization, Array.Empty<CustomizationOption>());
        object passport = passportTest.AddComponent(typeof(PassportManager));
        // In 1.1.10 this synchronous patch allocates fresh options and fit materials.
        // Snapshot just before invoking it, so even an exception before its final array
        // assignments can be cleaned up without destroying any pre-existing options.
        optionsBeforePassport = new HashSet<int>(Resources.FindObjectsOfTypeAll<CustomizationOption>().Select(option => option.GetInstanceID()));
        passportPatch.GetMethod("Awake", BindingFlags.NonPublic | BindingFlags.Static)!.Invoke(null, new[] { passport });
        var options = (CustomizationOption[])typeof(Customization).GetField("hats")!.GetValue(customization);
        var oursOptions = options.Where(o => o.name.StartsWith(Prefix, StringComparison.Ordinal)).ToArray();
        if (options.Length < customHats) throw new InvalidOperationException("Existing custom passport hats missing.");
        if (oursOptions.Length != 6 || oursOptions.Where((o,i) => o.name != hats[i].name || o.texture != hats[i].IconTexture).Any())
            throw new InvalidOperationException("Passport names/icons/order mismatch.");
        var allOptions = typeof(Customization).GetFields(BindingFlags.Public | BindingFlags.Instance)
            .Where(field => field.FieldType == typeof(CustomizationOption[]))
            .SelectMany(field => (CustomizationOption[])field.GetValue(customization));
        foreach (var category in originalCatalog!)
            foreach (var item in category.Value)
                if (!allOptions.Any(option => option.name == item.name))
                    throw new InvalidOperationException("Existing passport cosmetic was lost: " + item.name);
        results.Add($"isolatedPassportRegistration={options.Length}; jojoOptions=6; existing custom entries preserved; all JOJO icons and names match fixed order");
        }
        finally
        {
            var testOptions = optionsBeforePassport == null ? Array.Empty<CustomizationOption>() :
                Resources.FindObjectsOfTypeAll<CustomizationOption>()
                    .Where(option => !optionsBeforePassport!.Contains(option.GetInstanceID())).ToArray();
            var testMaterials = new HashSet<Material>();
            // Inspect sharedMaterials, not materials: this must not instantiate another copy.
            foreach (Renderer renderer in test.GetComponentsInChildren<Renderer>(true))
                foreach (Material material in renderer.sharedMaterials)
                    if (material && !originalMaterials.Contains(material.GetInstanceID())) testMaterials.Add(material);
            foreach (CustomizationOption option in testOptions)
                foreach (FieldInfo field in typeof(CustomizationOption).GetFields(BindingFlags.Public | BindingFlags.Instance))
                    if (field.FieldType == typeof(Material) && field.GetValue(option) is Material material &&
                        material && !originalMaterials.Contains(material.GetInstanceID())) testMaterials.Add(material);
            // FitMaterialFallback creates a new Material in 1.1.10. Only reclaim it
            // when this test initialized the cache; existing shared templates stay intact.
            if (materialCache.GetValue(null) is Material temporaryTemplate && temporaryTemplate &&
                !originalMaterials.Contains(temporaryTemplate.GetInstanceID())) testMaterials.Add(temporaryTemplate);
            try
            {
                SetStatic(typeof(MoreCustomizationsPlugin), nameof(MoreCustomizationsPlugin.BaseHatCount), savedBaseHatCount);
                SetStatic(typeof(MoreCustomizationsPlugin), nameof(MoreCustomizationsPlugin.OverrideHatCount), savedOverrideHatCount);
                shaderCache.SetValue(null, savedShader);
                materialCache.SetValue(null, savedMaterialTemplate);
                results.Add("isolatedFrameworkGlobalsRestored=PASS");
            }
            finally
            {
                // Never destroy shared meshes, textures, shaders or original materials.
                foreach (CustomizationOption option in testOptions) if (option) Object.Destroy(option);
                foreach (Material material in testMaterials) if (material) Object.Destroy(material);
                if (passportTest) Object.Destroy(passportTest);
                Object.Destroy(test);
            }
        }
    }
}

[Serializable]
internal sealed class MeshData
{
    public string name = "";
    public float[] positions = Array.Empty<float>();
    public int[] triangles = Array.Empty<int>();
    public float[] uv = Array.Empty<float>();
    public float[] normals = Array.Empty<float>();
    public string texture = "";
}
