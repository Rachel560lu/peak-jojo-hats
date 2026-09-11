using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace JojoHats;

/// <summary>
/// Adds our hats without replacing another pack's categories, objects, or ordering.
/// The framework uses positional cosmetic indices, so existing order is significant.
/// </summary>
internal static class CatalogMerge
{
    internal static IReadOnlyDictionary<TKey, IReadOnlyList<TValue>> Append<TKey, TValue>(
        IReadOnlyDictionary<TKey, IReadOnlyList<TValue>> existing,
        TKey hatType,
        IReadOnlyList<TValue> additions,
        Func<TValue, string> identity) where TKey : notnull
    {
        if (existing is null) throw new ArgumentNullException(nameof(existing));
        if (hatType is null) throw new ArgumentNullException(nameof(hatType));
        if (additions is null) throw new ArgumentNullException(nameof(additions));
        if (identity is null) throw new ArgumentNullException(nameof(identity));

        // Validate and snapshot all proposed additions before reading the existing
        // catalog. A malformed pack must never register only a partial subset.
        var proposed = new List<KeyValuePair<string, TValue>>(additions.Count);
        var additionIds = new HashSet<string>(StringComparer.Ordinal);
        for (int i = 0; i < additions.Count; i++)
        {
            TValue item = additions[i];
            if (item is null)
                throw new ArgumentException("An added cosmetic cannot be null.", nameof(additions));
            string id = identity(item);
            if (string.IsNullOrWhiteSpace(id))
                throw new ArgumentException("Every added cosmetic needs a non-empty identity.", nameof(additions));
            if (!additionIds.Add(id))
                throw new ArgumentException("Duplicate added cosmetic identity: " + id, nameof(additions));
            proposed.Add(new KeyValuePair<string, TValue>(id, item));
        }

        bool hasHats = existing.TryGetValue(hatType, out IReadOnlyList<TValue>? previousHats);
        if (hasHats && previousHats is null)
            throw new ArgumentException("The existing hat category cannot be null.", nameof(existing));

        var existingIds = new HashSet<string>(StringComparer.Ordinal);
        var mergedHats = new List<TValue>(hasHats ? previousHats!.Count + proposed.Count : proposed.Count);
        if (hasHats)
        {
            foreach (TValue item in previousHats!)
            {
                if (item is null)
                    throw new ArgumentException("An existing hat cannot be null.", nameof(existing));
                // Existing entries are owned by the framework/other mods. Keep
                // duplicates and unnamed entries as-is rather than repairing them.
                string id = identity(item);
                if (!string.IsNullOrWhiteSpace(id)) existingIds.Add(id);
                mergedHats.Add(item);
            }
        }

        int previousCount = mergedHats.Count;
        foreach (KeyValuePair<string, TValue> item in proposed)
            if (existingIds.Add(item.Key)) mergedHats.Add(item.Value);

        if (mergedHats.Count == previousCount) return existing;

        var next = new Dictionary<TKey, IReadOnlyList<TValue>>();
        foreach (KeyValuePair<TKey, IReadOnlyList<TValue>> category in existing)
            next.Add(category.Key, category.Value);
        next[hatType] = mergedHats.AsReadOnly();
        return new ReadOnlyDictionary<TKey, IReadOnlyList<TValue>>(next);
    }
}
