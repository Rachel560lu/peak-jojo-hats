using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using BepInEx;
using MoreCustomizations;
using UnityEngine;

namespace JojoHats.RuntimeProbe;

/// <summary>Read-only catalog probe for explicit isolated test launches; never ship in a release ZIP.</summary>
[BepInPlugin("midor.peak.jojohats.testprobe", "JOJO Hats Isolated Runtime Probe", "1.0.0")]
[BepInDependency("MoreCustomizations", "1.1.10")]
[BepInDependency("midor.peak.jojohats", BepInDependency.DependencyFlags.SoftDependency)]
public sealed class Plugin : BaseUnityPlugin
{
    private const string Prefix = "jojo_mvp_";
    private const string ExpectArgument = "--jojo-probe-expect-jojo=";
    private static readonly string[] ExpectedJojoNames =
    {
        Prefix + "01_jotaro_cap", Prefix + "02_josuke_pompadour", Prefix + "03_giorno_rolls",
        Prefix + "04_jonathan_hair", Prefix + "05_jolyne_buns", Prefix + "06_joseph_hair"
    };

    private void Awake()
    {
        string[] arguments = Environment.GetCommandLineArgs();
        if (!arguments.Contains("--jojo-probe-test", StringComparer.Ordinal)) return;

        // Do not read prior results, player names, configuration, or saved selections.
        File.WriteAllLines(ResultPath, new[] { "probeVersion=1.0.0", "result=PENDING" });
        StartCoroutine(ProbeAfterStartup(arguments));
    }

    private static string ResultPath => Path.Combine(Paths.BepInExRootPath, "jojo-probe.txt");

    private IEnumerator ProbeAfterStartup(string[] arguments)
    {
        yield return new WaitForSecondsRealtime(18);
        var lines = new List<string> { "probeVersion=1.0.0", "runtime=" + Application.unityVersion };
        try
        {
            InspectCatalog(arguments, lines);
            lines.Add("result=PASS");
        }
        catch (Exception error)
        {
            lines.Add("errorType=" + error.GetType().Name);
            lines.Add("error=" + Escape(error.Message));
            lines.Add("result=FAIL");
        }

        try
        {
            File.WriteAllLines(ResultPath, lines);
            Logger.LogInfo("JOJO_PROBE_FINISHED: " + lines.Last());
        }
        catch (Exception error)
        {
            Logger.LogError("JOJO_PROBE_WRITE_FAILED: " + error.GetType().Name);
        }
        finally
        {
            if (arguments.Contains("--jojo-test-quit", StringComparer.Ordinal)) Application.Quit();
        }
    }

    private static void InspectCatalog(string[] arguments, List<string> lines)
    {
        var catalog = MoreCustomizationsPlugin.AllCustomizationsData;
        lines.Add("frameworkInitialized=" + (catalog != null ? "True" : "False"));

        string[] expectedArgs = arguments.Where(a => a.StartsWith(ExpectArgument, StringComparison.Ordinal)).ToArray();
        if (expectedArgs.Length != 1 ||
            !int.TryParse(expectedArgs[0].Substring(ExpectArgument.Length), out int expectedCount) ||
            (expectedCount != 0 && expectedCount != 6))
            throw new InvalidOperationException("Supply exactly one --jojo-probe-expect-jojo=0 or --jojo-probe-expect-jojo=6 argument.");
        lines.Add("expectedJojo=" + expectedCount);
        if (catalog == null) throw new InvalidOperationException("More Customizations catalog did not initialize.");

        lines.Add("categoryCount=" + catalog.Count);
        int total = 0;
        int customHats = 0;
        var allJojoNames = new List<string>();
        var hatJojoNames = new List<string>();
        var serialized = new List<string>();
        var foreignSerialized = new SortedDictionary<string, string>(StringComparer.Ordinal);
        foreach (var category in catalog)
        {
            if (category.Value == null) throw new InvalidOperationException("A custom category contains a null list.");
            string key = category.Key.ToString();
            var names = new List<string>(category.Value.Count);
            foreach (var item in category.Value)
            {
                if (item == null) throw new InvalidOperationException("A custom catalog contains a null object.");
                // These are registered asset identities, not players or saved cosmetic choices.
                string name = item.name ?? string.Empty;
                names.Add(name);
                if (!name.StartsWith(Prefix, StringComparison.Ordinal)) continue;
                allJojoNames.Add(name);
                if (category.Key == Customization.Type.Hat) hatJojoNames.Add(name);
            }
            total += names.Count;
            if (category.Key == Customization.Type.Hat) customHats = names.Count;
            lines.Add("category." + key + ".count=" + names.Count);
            lines.Add("category." + key + ".names=" + JsonArray(names));
            serialized.Add(Quote(key) + ":" + JsonArray(names));
            string[] foreignNames = names.Where(name => !name.StartsWith(Prefix, StringComparison.Ordinal)).ToArray();
            // Canonicalize category keys only; entry order is intentionally never
            // sorted. Ignore empty categories so a new JOJO-only Hat category
            // cannot change the signature of the pre-existing foreign entries.
            if (foreignNames.Length > 0) foreignSerialized.Add(key, JsonArray(foreignNames));
        }
        lines.Add("totalCustomEntries=" + total);
        lines.Add("jojoCount=" + allJojoNames.Count);
        lines.Add("jojoHatCount=" + hatJojoNames.Count);
        lines.Add("customHatEntries=" + customHats);
        lines.Add("customNonHatEntries=" + (total - customHats));
        lines.Add("otherCustomEntries=" + (total - allJojoNames.Count));
        lines.Add("orderedNames={" + string.Join(",", serialized) + "}");
        lines.Add("foreignCatalog={" + string.Join(",", foreignSerialized.Select(pair => Quote(pair.Key) + ":" + pair.Value)) + "}");

        if (allJojoNames.Count != expectedCount || hatJojoNames.Count != expectedCount)
            throw new InvalidOperationException("JOJO counts do not match the explicit expected hat count.");
        if (expectedCount == 6 && !hatJojoNames.SequenceEqual(ExpectedJojoNames, StringComparer.Ordinal))
            throw new InvalidOperationException("The six JOJO asset identities are duplicated, missing, or in an unexpected order.");
    }

    private static string JsonArray(IEnumerable<string> values) => "[" + string.Join(",", values.Select(Quote)) + "]";
    private static string Quote(string value) => "\"" + Escape(value) + "\"";
    private static string Escape(string value)
    {
        var output = new StringBuilder(value.Length);
        foreach (char character in value)
        {
            switch (character)
            {
                case '\\': output.Append("\\\\"); break;
                case '"': output.Append("\\\""); break;
                case '\r': output.Append("\\r"); break;
                case '\n': output.Append("\\n"); break;
                case '\t': output.Append("\\t"); break;
                default:
                    if (character < 0x20) output.Append("\\u" + ((int)character).ToString("x4"));
                    else output.Append(character);
                    break;
            }
        }
        return output.ToString();
    }
}
