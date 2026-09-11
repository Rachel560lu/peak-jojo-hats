using System;
using System.Collections.Generic;
using System.Reflection;
using MoreCustomizations;

namespace JojoHats;

/// <summary>
/// Explicit smoke-test helper only. Exercises the game's cosmetic wire format locally;
/// it neither sends a packet nor proves two-client/late-join compatibility.
/// </summary>
internal static class NetworkIndexSmoke
{
    private static readonly string[] HatNames = {
        "jojo_mvp_01_jotaro_cap", "jojo_mvp_02_josuke_pompadour",
        "jojo_mvp_03_giorno_rolls", "jojo_mvp_04_jonathan_hair",
        "jojo_mvp_05_jolyne_buns", "jojo_mvp_06_joseph_hair"
    };

    private static readonly string[] FieldNames = {
        "currentSkin", "currentAccessory", "currentEyes", "currentMouth",
        "currentOutfit", "currentHat", "currentSash", "currentMedal"
    };

    internal static void Verify(List<string> results, int firstJojoRuntimeIndex)
    {
        if (results == null) throw new ArgumentNullException(nameof(results));

        // Resolve the existing singleton, never create/assign a test singleton.
        // Reflection also keeps this test from adding a shipped Zorro dependency.
        // Read the backing field directly: the Instance getter can discover/cache an
        // object and call OnCreated when empty, which is forbidden in this test.
        FieldInfo instanceField = typeof(Customization).BaseType?.GetField(
            "_instance", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)
            ?? throw new MissingFieldException("Customization singleton _instance");
        FieldInfo shuttingDownField = typeof(Customization).BaseType?.GetField(
            "m_shuttingDown", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)
            ?? throw new MissingFieldException("Customization singleton m_shuttingDown");
        var customization = instanceField.GetValue(null) as Customization;
        if (customization is null || (object)customization is not UnityEngine.Object unityObject ||
            !unityObject || (bool)shuttingDownField.GetValue(null)!)
            throw new InvalidOperationException("Local serialization test needs the real Customization singleton.");

        int baseHats = MoreCustomizationsPlugin.BaseHatCount;
        int overrideHats = MoreCustomizationsPlugin.OverrideHatCount;
        if (baseHats <= 0 || overrideHats < 0 || firstJojoRuntimeIndex < baseHats + overrideHats)
            throw new InvalidOperationException("Local serialization test has invalid vanilla/override hat bounds.");
        int firstMenuIndex = firstJojoRuntimeIndex - overrideHats;
        if (customization.hats == null || firstMenuIndex < 0 ||
            firstMenuIndex > customization.hats.Length - HatNames.Length)
            throw new InvalidOperationException("JOJO runtime indices do not fit the real passport catalog.");
        for (int i = 0; i < HatNames.Length; i++)
            if (!customization.hats[firstMenuIndex + i] ||
                customization.hats[firstMenuIndex + i].name != HatNames[i])
                throw new InvalidOperationException("JOJO menu/runtime index mapping differs at ordinal " + i);

        // All other fields stay at a valid vanilla zero. CorrectValues must see the
        // working game catalog, rather than a fake empty passport used by other tests.
        foreach (string fieldName in new[] { "skins", "accessories", "eyes", "mouths", "fits", "sashes", "medals" })
        {
            var options = typeof(Customization).GetField(fieldName)?.GetValue(customization) as CustomizationOption[];
            if (options == null || options.Length == 0)
                throw new InvalidOperationException("Real customization category unavailable: " + fieldName);
        }

        Type dataType = typeof(CharacterCustomizationData);
        MethodInfo serialize = dataType.GetMethod("Serialize", BindingFlags.Public | BindingFlags.Instance)
            ?? throw new MissingMethodException(dataType.FullName, "Serialize");
        MethodInfo deserialize = dataType.GetMethod("Deserialize", BindingFlags.Public | BindingFlags.Instance)
            ?? throw new MissingMethodException(dataType.FullName, "Deserialize");
        Type serializerType = serialize.GetParameters()[0].ParameterType;
        Type deserializerType = deserialize.GetParameters()[0].ParameterType;
        ConstructorInfo readerConstructor = deserializerType.GetConstructor(new[] { serializerType })
            ?? throw new MissingMethodException(deserializerType.FullName, ".ctor(BinarySerializer)");
        PropertyInfo position = serializerType.GetProperty("Position")
            ?? throw new MissingMemberException(serializerType.FullName, "Position");
        var fields = new FieldInfo[FieldNames.Length];
        for (int i = 0; i < fields.Length; i++)
        {
            fields[i] = dataType.GetField(FieldNames[i], BindingFlags.Public | BindingFlags.Instance)
                ?? throw new MissingFieldException(dataType.FullName, FieldNames[i]);
            if (fields[i].FieldType != typeof(int))
                throw new InvalidOperationException("Game cosmetic format changed: " + FieldNames[i]);
        }

        for (int ordinal = 0; ordinal < HatNames.Length; ordinal++)
        {
            int hatIndex = checked(firstJojoRuntimeIndex + ordinal);
            object source = Activator.CreateInstance(dataType)!;
            object received = Activator.CreateInstance(dataType)!;
            fields[5].SetValue(source, hatIndex);
            object serializer = Activator.CreateInstance(serializerType)!;
            try
            {
                serialize.Invoke(source, new[] { serializer });
                if ((int)position.GetValue(serializer)! != FieldNames.Length * sizeof(int))
                    throw new InvalidOperationException("Game cosmetic serialization byte count changed.");

                // This constructor BORROWS the serializer's NativeArray. Do not call
                // reader.Dispose(): that would double-free the serializer-owned buffer.
                // The reader has no finalizer; only the owning serializer is disposed.
                object reader = readerConstructor.Invoke(new[] { serializer });
                deserialize.Invoke(received, new[] { reader });
                for (int fieldIndex = 0; fieldIndex < fields.Length; fieldIndex++)
                {
                    int expected = fieldIndex == 5 ? hatIndex : 0;
                    if ((int)fields[fieldIndex].GetValue(source)! != expected ||
                        (int)fields[fieldIndex].GetValue(received)! != expected)
                        throw new InvalidOperationException("Local cosmetic round-trip changed " +
                            FieldNames[fieldIndex] + " for " + HatNames[ordinal]);
                }
            }
            finally
            {
                ((IDisposable)serializer).Dispose();
            }
        }

        results.Add("localGameSerializationRoundTrip=6/6; actual Serialize/Deserialize+CorrectValues; " +
            "runtimeIndices=" + firstJojoRuntimeIndex + ".." + (firstJojoRuntimeIndex + HatNames.Length - 1) +
            "; saves=untouched; packetsSent=0; twoClientMultiplayer=NOT_TESTED");
    }
}
