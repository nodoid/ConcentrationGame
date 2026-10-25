#if SCREENSHOTS
using Concentration.Enums;
using Concentration.ViewModels;

namespace Concentration.Helpers
{
    // Plays real moves to put the game into a known state for store screenshots.
    // Only compiled with -p:Screenshots=true; the shot is chosen with the CONC_SHOT
    // environment variable (iOS simulator / Mac) or the "shot" intent extra (Android).
    //   title  - the start screen
    //   board  - a Medium game: one pair found and a card turned
    //   play   - an Easy game part-way through: one miss, four pairs found, a card turned
    //   win    - a Hard game cleared, with the Reset and High Scores buttons
    //   scores - the win followed by the high score table
    //   demo   - a whole Medium game at a human pace for the app preview video, logging
    //            each sound (with its Unix time in ms) to demo-events.txt in AppDataDirectory
    public static class ScreenshotDriver
    {
        public static string Shot { get; set; } = Environment.GetEnvironmentVariable("CONC_SHOT") ?? "";

        static readonly string EventLog = Path.Combine(FileSystem.AppDataDirectory, "demo-events.txt");

        public static void Log(string evt)
        {
            if (Shot == "demo")
                File.AppendAllText(EventLog, $"{DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()} {evt}\n");
        }

        public static async Task OnMainPage(StartupViewModel vm)
        {
            if (Shot is "" or "title")
                return;
            if (Shot == "demo")
            {
                File.Delete(EventLog);
                // OnAppearing comes well before the first frame: the background takes a while to draw
                await Task.Delay(4000);
                Log("title");
                await Task.Delay(3000);
            }
            else
                await Task.Delay(500);
            var level = Shot switch { "board" or "demo" => "1", "play" => "0", _ => "2" };
            await MainThread.InvokeOnMainThreadAsync(() => vm.SetDifficultyCommand.ExecuteAsync(level));
        }

        public static async Task OnGame(GameViewModel vm)
        {
            if (Shot is "" or "title")
                return;
            while (vm.Tiles.Count < 16 || vm.DifficultGuesses == "")
                await Task.Delay(50);
            await Task.Delay(1000);

            var tiles = vm.Tiles.ToList();
            var pairs = tiles.Distinct().Select(name => (tiles.IndexOf(name), tiles.LastIndexOf(name))).ToList();

            async Task Turn(int tile) => await MainThread.InvokeOnMainThreadAsync(() => vm.TileSelectedCommand.ExecuteAsync(tile.ToString()));

            switch (Shot)
            {
                case "demo":
                    await Demo(pairs, Turn);
                    await Task.Delay(2500);
                    await MainThread.InvokeOnMainThreadAsync(() => vm.ShowHighScoresCommand.ExecuteAsync(null));
                    Log("scores");
                    break;
                case "board":
                    await Turn(pairs[3].Item1);
                    await Turn(pairs[3].Item2);
                    await Turn(pairs[5].Item1);
                    break;
                case "play":
                    await Turn(pairs[0].Item1);
                    await Turn(pairs[1].Item1);
                    await Task.Delay(300);
                    foreach (var (a, b) in pairs.Skip(2).Take(4))
                    {
                        await Turn(a);
                        await Turn(b);
                    }
                    await Turn(pairs[7].Item1);
                    break;
                default:
                    foreach (var (a, b) in pairs)
                    {
                        await Turn(a);
                        await Turn(b);
                    }
                    if (Shot == "scores")
                    {
                        await Task.Delay(1500);
                        await MainThread.InvokeOnMainThreadAsync(() => vm.ShowHighScoresCommand.ExecuteAsync(null));
                    }
                    break;
            }
        }

        // A player with a perfect memory but no foresight: turn an unseen card, then its partner if
        // it has been seen, otherwise another unseen card. After a few misses the player "gets lucky"
        // so a Medium game (10 misses allowed) is always won and the video stays under 30 seconds.
        static async Task Demo(List<(int, int)> pairs, Func<int, Task> turn)
        {
            var partner = new Dictionary<int, int>();
            foreach (var (a, b) in pairs)
            {
                partner[a] = b;
                partner[b] = a;
            }
            var unseen = new List<int> { 5, 10, 0, 15, 6, 3, 12, 9, 1, 14, 7, 8, 2, 13, 4, 11 };
            var seen = new HashSet<int>();
            var found = new HashSet<int>();
            var misses = 0;
            const int pace = 600;

            async Task Turn(int tile)
            {
                await turn(tile);
                Log("turn");
                unseen.Remove(tile);
                seen.Add(tile);
                await Task.Delay(pace);
            }

            while (found.Count < 16)
            {
                // a pair already seen on the board is picked up straight away
                var known = seen.FirstOrDefault(t => !found.Contains(t) && seen.Contains(partner[t]), -1);
                if (known >= 0)
                {
                    await Turn(known);
                    await Turn(partner[known]);
                    found.UnionWith(new[] { known, partner[known] });
                    continue;
                }
                var first = unseen.First();
                await Turn(first);
                if (seen.Contains(partner[first]))
                {
                    await Turn(partner[first]);
                }
                else
                {
                    var second = misses >= 4 ? partner[first] : unseen.FirstOrDefault(t => t != partner[first], partner[first]);
                    await Turn(second);
                    if (second != partner[first])
                    {
                        misses++; // the game held the pair for a second before turning it back
                        continue;
                    }
                }
                found.UnionWith(new[] { first, partner[first] });
            }
        }
    }
}
#endif
