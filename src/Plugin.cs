using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using BepInEx;
using MoreCustomizations;
using MoreCustomizations.Data;
using UnityEngine;
using Object = UnityEngine.Object;

namespace JojoHats;

[BepInPlugin("midor.peak.jojohats", "JOJO Scout Hats", "0.4.2")]
[BepInDependency("MoreCustomizations", "1.1.10")]
public sealed class Plugin : BaseUnityPlugin
{
    private const string Prefix = "jojo_mvp_";
    private static readonly string[] Ids = {
        "01_jotaro_cap", "02_josuke_pompadour", "03_giorno_rolls",
        "04_jonathan_hair", "05_jolyne_buns", "06_joseph_hair"
    };
    private readonly List<Object> ownedAssets = new();
    private readonly List<CustomHat_V1> hats = new();
    private GameObject? templates;

    private void Awake()
    {
        try
        {
            string root = Path.Combine(Path.GetDirectoryName(Info.Location)!, "assets");
            var previous = MoreCustomizationsPlugin.AllCustomizationsData
                ?? throw new InvalidOperationException("More Customizations did not initialize. See docs/INSTALL.md and the release's scripts/install-jojo-only.ps1 for the empty-bundle compatibility step.");
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
                hat.name = Prefix + id;
                Set(hat, nameof(CustomHat_V1.Icon), LoadTexture(Path.Combine(folder, "icon.png")));
                Set(hat, nameof(CustomHat_V1.Prefab), prefab);
                Set(hat, nameof(CustomHat_V1.MainTexture), main);
                Set(hat, nameof(CustomHat_V1.SubTexture), main);
                Set(hat, nameof(CustomHat_V1.PositionOffset), Vector3.zero);
                Set(hat, nameof(CustomHat_V1.EulerAngleOffset), Vector3.zero);
                if (!hat.IsValid) throw new InvalidDataException("Hat validation failed: " + id);
                ownedAssets.Add(hat);
                hats.Add(hat);
                Logger.LogInfo($"Prepared {id}: {mesh.vertexCount} vertices, {data.triangles.Length / 3} triangles");
            }
            // This is deliberately a JOJO-only custom profile. Vanilla catalogs remain intact.
            var next = new Dictionary<Customization.Type, IReadOnlyList<CustomizationData>>();
            var allHats = new List<CustomizationData>();
            allHats.AddRange(hats);
            next[Customization.Type.Hat] = allHats.AsReadOnly();
            // 1.1.10 has no public RegisterHat API. Isolate the private setter bridge here.
            // Exclude all framework examples/other custom packs; do not alter vanilla entries.
            SetStatic(typeof(MoreCustomizationsPlugin), "AllCustomizationsData", next);
            Logger.LogInfo("JOJO_REGISTERED=6; catalog order fixed; ready for passport and character creation.");
            if (Environment.GetCommandLineArgs().Contains("--jojo-smoke-test"))
            {
                File.WriteAllLines(Path.Combine(Paths.BepInExRootPath, "jojo-smoke.txt"), new[] { "version=0.4.2", "result=PENDING" });
                StartCoroutine(SmokeTest());
            }
        }
        catch (Exception e)
        {
            Logger.LogError("JOJO initialization aborted before registration: " + e);
            if (templates) Object.Destroy(templates);
            foreach (Object asset in ownedAssets) if (asset) Object.Destroy(asset);
            enabled = false;
        }
    }

    private Texture2D LoadTexture(string path)
    {
        var texture = new Texture2D(2, 2, TextureFormat.RGBA32, false);
        if (!ImageConversion.LoadImage(texture, File.ReadAllBytes(path)))
            throw new InvalidDataException("Cannot decode " + path);
        texture.name = Path.GetFileName(path);
        texture.wrapMode = TextureWrapMode.Clamp;
        ownedAssets.Add(texture);
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
        var mesh = new Mesh { name = Prefix + data.name, vertices = vertices, uv = uv, colors = colors };
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
        ownedAssets.Add(mesh);
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
        var results = new List<string> { "version=0.4.2", "registered=" + hats.Count };
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
            if (other != 0 || catalog[Customization.Type.Hat].Count != 6)
                throw new InvalidOperationException("JOJO-only catalog invariant failed.");
            if (Directory.GetFiles(Paths.PluginPath, "*.pcab", SearchOption.AllDirectories).Length != 0)
                throw new InvalidOperationException("Isolated profile still contains a pcab bundle.");
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

    private void IntegrationSmoke(List<string> results)
    {
        GameObject source = Resources.Load<GameObject>("Character");
        if (!source) throw new InvalidOperationException("Game Character prefab not found.");
        // Clone inactive: do not run gameplay/network Awake, create a player, or alter saves.
        GameObject test = Object.Instantiate(source, templates!.transform, false);
        test.name = "JOJO isolated prefab integration";
        var cc = test.GetComponent<CharacterCustomization>();
        if (!cc || !cc.refs) throw new InvalidOperationException("CharacterCustomization refs missing.");
        int original = cc.refs.playerHats.Length;
        Type patch = typeof(MoreCustomizationsPlugin).Assembly.GetType("MoreCustomizations.Patches.CharacterCustomizationPatch", true);
        patch.GetMethod("Awake", BindingFlags.Static | BindingFlags.NonPublic)!.Invoke(null, new object[] { cc });
        Renderer[] ours = cc.refs.playerHats.Where(r => r && r.name.StartsWith(Prefix, StringComparison.Ordinal)).ToArray();
        if (ours.Length != 6) throw new InvalidOperationException("Not all six hats attached to actual Character prefab.");
        if (cc.refs.playerHats.Length != original + 6) throw new InvalidOperationException("Unexpected extra hat renderer.");
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
        // Exercise the framework's passport registration against an isolated empty catalog.
        // This checks icon/type/name registration, not interactive passport UI navigation.
        GameObject passportTest = new GameObject("JOJO isolated passport registration");
        passportTest.transform.SetParent(templates.transform, false);
        object customization = passportTest.AddComponent(typeof(Customization));
        foreach (FieldInfo field in typeof(Customization).GetFields(BindingFlags.Public | BindingFlags.Instance))
            if (field.FieldType == typeof(CustomizationOption[])) field.SetValue(customization, Array.Empty<CustomizationOption>());
        object passport = passportTest.AddComponent(typeof(PassportManager));
        Type passportPatch = typeof(MoreCustomizationsPlugin).Assembly.GetType("MoreCustomizations.Patches.PassportManagerPatch", true);
        passportPatch.GetMethod("Awake", BindingFlags.NonPublic | BindingFlags.Static)!.Invoke(null, new[] { passport });
        var options = (CustomizationOption[])typeof(Customization).GetField("hats")!.GetValue(customization);
        var oursOptions = options.Where(o => o.name.StartsWith(Prefix, StringComparison.Ordinal)).ToArray();
        if (options.Length != 6) throw new InvalidOperationException("Unexpected non-JOJO custom passport hats.");
        foreach (FieldInfo field in typeof(Customization).GetFields(BindingFlags.Public | BindingFlags.Instance))
            if (field.FieldType == typeof(CustomizationOption[]) && field.Name != "hats" && ((CustomizationOption[])field.GetValue(customization)).Length != 0)
                throw new InvalidOperationException("Unexpected custom cosmetics in " + field.Name);
        if (oursOptions.Length != 6 || oursOptions.Where((o,i) => o.name != hats[i].name || o.texture != hats[i].IconTexture).Any())
            throw new InvalidOperationException("Passport names/icons/order mismatch.");
        results.Add("isolatedPassportRegistration=6; all icons and names match fixed hat order");
        Object.Destroy(passportTest);
        Object.Destroy(test);
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
