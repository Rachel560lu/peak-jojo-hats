using System.Collections.ObjectModel;
using JojoHats;

var tests = new (string Name, Action Run)[]
{
    ("preserves other categories and all existing object references", PreservesExistingCatalog),
    ("never changes original dictionary, lists, or addition list", LeavesInputsUntouched),
    ("repeated registration is idempotent", IsIdempotent),
    ("does not globally sort existing hats or supplied additions", DoesNotSort),
    ("appends an absent hat category", AddsMissingCategory),
    ("empty additions are a no-op, including absent category", EmptyAdditionsAreNoOp),
    ("existing identity wins a collision without replacement", PreservesCollisions),
    ("existing duplicate IDs remain intact", PreservesExistingDuplicates),
    ("identity collisions in other categories do not suppress hats", IgnoresOtherCategoryIds),
    ("identity comparison is ordinal and case-sensitive", UsesOrdinalIdentity),
    ("null arguments are rejected", RejectsNullArguments),
    ("blank addition IDs are rejected atomically", RejectsBlankIdentities),
    ("duplicate addition IDs are rejected even if already registered", RejectsDuplicateAdditions),
    ("null added entries are rejected", RejectsNullAddition),
    ("invalid existing hat collections are rejected", RejectsMalformedExistingHats),
    ("existing unnamed hats remain untouched", PreservesUnnamedExistingHats),
    ("identity exception leaves original catalog untouched", IdentityFailureIsAtomic),
    ("same ordered inputs produce stable ordered output", HasStableOutput),
    ("legacy exclusive catalog retains all six original objects", PreservesLegacyExclusiveCatalog),
    ("published dictionary and merged hat list are read-only", ReturnsReadOnlyCollections),
    ("non-hat identities are never inspected", DoesNotInspectOtherCategories),
    ("copied dictionary and merged hat list are independent snapshots", CopiesChangedCollections),
};

int failures = 0;
foreach (var test in tests)
{
    try { test.Run(); Console.WriteLine("PASS " + test.Name); }
    catch (Exception error)
    {
        failures++;
        Console.Error.WriteLine("FAIL " + test.Name + ": " + error);
    }
}
Console.WriteLine($"CatalogMerge: {tests.Length - failures}/{tests.Length} tests passed.");
return failures == 0 ? 0 : 1;

static IReadOnlyDictionary<Kind, IReadOnlyList<Hat>> Merge(
    IReadOnlyDictionary<Kind, IReadOnlyList<Hat>> source, IReadOnlyList<Hat> additions)
    => CatalogMerge.Append(source, Kind.Hat, additions, h => h.Id);

static (Dictionary<Kind, IReadOnlyList<Hat>> Catalog, List<Hat> Hats, Hat[] Additions) Fixture()
{
    var hats = new List<Hat> { new("third-party-z"), new("built-in"), new("third-party-a") };
    return (new Dictionary<Kind, IReadOnlyList<Hat>>
    {
        [Kind.Eyes] = new[] { new Hat("eyes-2"), new Hat("eyes-1") },
        [Kind.Hat] = hats,
        [Kind.Outfit] = new[] { new Hat("outfit") },
        [Kind.Mouth] = Array.Empty<Hat>(),
        [Kind.Accessory] = new[] { new Hat("glasses") },
    }, hats, new[] { new Hat("jojo-02"), new Hat("jojo-01") });
}

static void PreservesExistingCatalog()
{
    var (source, hats, additions) = Fixture();
    var result = Merge(source, additions);
    Equal(source.Count, result.Count);
    SameSequence(source.Keys, result.Keys);
    foreach (var category in source)
    {
        if (category.Key == Kind.Hat) continue;
        Same(category.Value, result[category.Key]);
    }
    SameObjects(hats.Concat(additions), result[Kind.Hat]);
}

static void LeavesInputsUntouched()
{
    var (source, hats, additions) = Fixture();
    var entriesBefore = source.ToArray();
    var hatsBefore = hats.ToArray();
    var additionsBefore = additions.ToArray();
    _ = Merge(source, additions);
    SameSequence(entriesBefore, source);
    Same(source[Kind.Hat], hats);
    SameObjects(hatsBefore, hats);
    SameObjects(additionsBefore, additions);
}

static void IsIdempotent()
{
    var (source, _, additions) = Fixture();
    var once = Merge(source, additions);
    var twice = Merge(once, additions);
    Same(once, twice);
    Equal(source[Kind.Hat].Count + additions.Length, twice[Kind.Hat].Count);
}

static void DoesNotSort()
{
    var (source, _, additions) = Fixture();
    SameSequence(new[] { "third-party-z", "built-in", "third-party-a", "jojo-02", "jojo-01" },
        Merge(source, additions)[Kind.Hat].Select(h => h.Id));
}

static void AddsMissingCategory()
{
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Eyes] = new[] { new Hat("eye") } };
    var additions = new[] { new Hat("jojo") };
    var result = Merge(source, additions);
    Same(source[Kind.Eyes], result[Kind.Eyes]);
    SameSequence(new[] { Kind.Eyes, Kind.Hat }, result.Keys);
    SameObjects(additions, result[Kind.Hat]);
    Equal(1, source.Count);
    Assert(!source.ContainsKey(Kind.Hat), "Source must not acquire a Hat key.");
}

static void EmptyAdditionsAreNoOp()
{
    var (source, _, _) = Fixture();
    Same(source, Merge(source, Array.Empty<Hat>()));
    var empty = new Dictionary<Kind, IReadOnlyList<Hat>>();
    Same(empty, Merge(empty, Array.Empty<Hat>()));
    Equal(0, empty.Count);
}

static void PreservesCollisions()
{
    var old = new Hat("jojo-01");
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new[] { old } };
    var newHat = new Hat("jojo-02");
    var result = Merge(source, new[] { new Hat("jojo-01"), newHat });
    SameObjects(new[] { old, newHat }, result[Kind.Hat]);
}

static void PreservesExistingDuplicates()
{
    var first = new Hat("same");
    var second = new Hat("same");
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new[] { first, second } };
    var addition = new Hat("new");
    SameObjects(new[] { first, second, addition }, Merge(source, new[] { new Hat("same"), addition })[Kind.Hat]);
}

static void IgnoresOtherCategoryIds()
{
    var eye = new Hat("same");
    var hat = new Hat("same");
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Eyes] = new[] { eye } };
    var result = Merge(source, new[] { hat });
    Same(hat, result[Kind.Hat][0]);
    Same(eye, result[Kind.Eyes][0]);
}

static void UsesOrdinalIdentity()
{
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new[] { new Hat("JOJO") } };
    Equal(2, Merge(source, new[] { new Hat("jojo") })[Kind.Hat].Count);
}

static void RejectsNullArguments()
{
    var source = new Dictionary<Kind, IReadOnlyList<Hat>>();
    Throws<ArgumentNullException>(() => Merge(null!, Array.Empty<Hat>()), "existing");
    Throws<ArgumentNullException>(() => Merge(source, null!), "additions");
    Throws<ArgumentNullException>(() => CatalogMerge.Append(source, Kind.Hat, Array.Empty<Hat>(), null!), "identity");
    Throws<ArgumentNullException>(() => CatalogMerge.Append(
        new Dictionary<string, IReadOnlyList<Hat>>(), null!, Array.Empty<Hat>(), h => h.Id), "hatType");
}

static void RejectsBlankIdentities()
{
    foreach (string? invalidId in new[] { null, "", " ", "\t\r\n" })
    {
        var (source, hats, _) = Fixture();
        var before = hats.ToArray();
        int existingReads = 0;
        Throws<ArgumentException>(() => CatalogMerge.Append(source, Kind.Hat,
            new[] { new Hat("valid"), new Hat(invalidId!) }, hat =>
            {
                if (hats.Contains(hat)) existingReads++;
                return hat.Id;
            }), "additions");
        SameObjects(before, hats);
        Equal(0, existingReads);
    }
}

static void RejectsDuplicateAdditions()
{
    var old = new Hat("already-here");
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new[] { old } };
    Throws<ArgumentException>(() => Merge(source, new[] { new Hat("already-here"), new Hat("already-here") }), "additions");
    SameObjects(new[] { old }, source[Kind.Hat]);
}

static void RejectsNullAddition()
{
    var (source, _, _) = Fixture();
    Throws<ArgumentException>(() => Merge(source, new Hat[] { new("valid"), null! }), "additions");
}

static void RejectsMalformedExistingHats()
{
    Throws<ArgumentException>(() => Merge(
        new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = null! }, new[] { new Hat("new") }), "existing");
    Throws<ArgumentException>(() => Merge(
        new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new Hat[] { null! } }, new[] { new Hat("new") }), "existing");
}

static void PreservesUnnamedExistingHats()
{
    var old = new Hat(null!);
    var newHat = new Hat("new");
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = new[] { old } };
    SameObjects(new[] { old, newHat }, Merge(source, new[] { newHat })[Kind.Hat]);
}

static void IdentityFailureIsAtomic()
{
    var (source, hats, _) = Fixture();
    var before = hats.ToArray();
    Throws<InvalidOperationException>(() => CatalogMerge.Append(source, Kind.Hat,
        new[] { new Hat("good"), new Hat("explode") }, hat =>
            hat.Id == "explode" ? throw new InvalidOperationException("test") : hat.Id));
    SameObjects(before, source[Kind.Hat]);
    Equal(5, source.Count);
}

static void HasStableOutput()
{
    var (source, _, additions) = Fixture();
    var expected = Merge(source, additions)[Kind.Hat];
    for (int i = 0; i < 10; i++) SameObjects(expected, Merge(source, additions)[Kind.Hat]);
}

static void PreservesLegacyExclusiveCatalog()
{
    string[] ids = { "01_jotaro_cap", "02_josuke_pompadour", "03_giorno_rolls", "04_jonathan_hair", "05_jolyne_buns", "06_joseph_hair" };
    var old = ids.Select(id => new Hat("jojo_mvp_" + id)).ToArray();
    var source = new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Hat] = old };
    var fresh = ids.Select(id => new Hat("jojo_mvp_" + id)).ToArray();
    var result = Merge(source, fresh);
    Same(source, result);
    SameObjects(old, result[Kind.Hat]);
    Equal(6, result[Kind.Hat].Count);
}

static void ReturnsReadOnlyCollections()
{
    var (source, _, additions) = Fixture();
    var result = Merge(source, additions);
    Throws<NotSupportedException>(() => ((IDictionary<Kind, IReadOnlyList<Hat>>)result).Add(Kind.Other, Array.Empty<Hat>()));
    Throws<NotSupportedException>(() => ((IList<Hat>)result[Kind.Hat]).Add(new Hat("extra")));
}

static void DoesNotInspectOtherCategories()
{
    var eye = new Hat("eye");
    var source = new ReadOnlyDictionary<Kind, IReadOnlyList<Hat>>(
        new Dictionary<Kind, IReadOnlyList<Hat>> { [Kind.Eyes] = new[] { eye } });
    var result = CatalogMerge.Append(source, Kind.Hat, new[] { new Hat("hat") }, item =>
        ReferenceEquals(item, eye) ? throw new InvalidOperationException("Inspected an unrelated category") : item.Id);
    Same(source[Kind.Eyes], result[Kind.Eyes]);
}

static void CopiesChangedCollections()
{
    var (source, hats, additions) = Fixture();
    var result = Merge(source, additions);
    source.Remove(Kind.Eyes);
    hats.Add(new Hat("late"));
    additions[0] = new Hat("replacement");
    Equal(5, result.Count);
    Equal(5, result[Kind.Hat].Count);
    Equal("jojo-02", result[Kind.Hat][3].Id);
}

static void Assert(bool condition, string message)
{
    if (!condition) throw new Exception(message);
}

static void Equal<T>(T expected, T actual)
    => Assert(EqualityComparer<T>.Default.Equals(expected, actual), $"Expected {expected}, got {actual}.");

static void Same(object expected, object actual)
    => Assert(ReferenceEquals(expected, actual), "Expected the same object reference.");

static void SameSequence<T>(IEnumerable<T> expected, IEnumerable<T> actual)
    => Assert(expected.SequenceEqual(actual), "Sequence values/order differ.");

static void SameObjects(IEnumerable<Hat> expected, IEnumerable<Hat> actual)
{
    Hat[] left = expected.ToArray(), right = actual.ToArray();
    Equal(left.Length, right.Length);
    for (int i = 0; i < left.Length; i++) Same(left[i], right[i]);
}

static void Throws<TException>(Action action, string? paramName = null) where TException : Exception
{
    try { action(); }
    catch (TException error)
    {
        if (paramName is not null) Equal(paramName, ((ArgumentException)(object)error).ParamName);
        return;
    }
    throw new Exception("Expected " + typeof(TException).Name + ".");
}

enum Kind { Hat, Eyes, Outfit, Mouth, Accessory, Other }
sealed class Hat(string id) { public string Id { get; } = id; }
