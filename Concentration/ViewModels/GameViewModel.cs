using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Concentration.Enums;
using Concentration.Helpers;
using Concentration.Interfaces;
using Concentration.Models;
using Plugin.Maui.Audio;
using System.Collections.ObjectModel;

namespace Concentration.ViewModels
{
    public partial class GameViewModel : BaseViewModel
    {
        IRepository? repository;

        [ObservableProperty]
        bool showButton;

        [ObservableProperty]
        string numGuesses;

        [ObservableProperty]
        string difficultGuesses;

        [ObservableProperty]
        ObservableCollection<string> tiles = new ObservableCollection<string>();

        [ObservableProperty]
        string imageOne;

        [ObservableProperty] 
        string imageTwo;

        [ObservableProperty]
        bool resetBoard;

        [ObservableProperty]
        int score;

        int highScoreTable { get; set; }

        int guesses { get; set; }

        int correctGuesses { get; set; } 

        [ObservableProperty]
        int tileOne  = -1;
        [ObservableProperty]
        int tileTwo  = -1;

        [ObservableProperty]
        int numguess = 0;
        [ObservableProperty]
        Tuple<int, int> lastGuesses;

        ObservableCollection<HighScoreModel> HighScores { get; set; }


        Random random = new Random();

        [RelayCommand]
        public async Task ButtonPressed()
        {
            await PlayAudio("scream");
            Tiles.Clear();
            ResetBoard = true;
            ShowButton = false;
            ShuffleTiles();
            guesses = Score = correctGuesses = 0;
            highScoreTable = 0;
            TileOne = TileTwo = -1;
            NumGuesses = $"Wrong Guesses : {guesses}";
        }

        [RelayCommand]
        public async Task TileSelected(string tile)
        {
            await PlayAudio("slice");
            LastGuesses = new Tuple<int, int>(-1, -1);
            if (TileOne == -1)
            {
                var tile1 = Convert.ToInt32(tile);
                ShowTile(tile1);
                TileOne = tile1;
            }
            else
            {
                var tile2 = Convert.ToInt32(tile);
                ShowTile(tile2, true);
                TileTwo = tile2;
            }
            if (TileTwo != -1)
            {
                if (Tiles[TileOne].Equals(Tiles[TileTwo]))
                {
                    Score++;
                    correctGuesses++;
                    highScoreTable = Score * (DifficultLevel == Difficulty.Hard ? 20 :
                        (DifficultLevel == Difficulty.Medium ? 10 : 5));
                    TileOne = TileTwo = -1;
                }
                else
                {
                    guesses++;
                    NumGuesses = $"Wrong Guesses : {guesses}";
                    await Task.Delay(1000);
                    LastGuesses = new Tuple<int, int>(TileOne, TileTwo);
                    TileOne = TileTwo = -1;
                }
            }
            if (guesses == (int)DifficultLevel || correctGuesses == 8)
            {
                ShowButton = true;

                CheckHiScore();

                if (Score != Numguess)
                {
                    await PlayAudio("creepyGirl");
                }
                else
                {
                    await PlayAudio("wolves");
                }
            }
        }

        [RelayCommand]
        public async Task ShowHighScores() => await Mopups.Services.MopupService.Instance.PushAsync(new Views.Popups.HiscoreTables(), true);

        public GameViewModel()
        {
            repository = App.Service.GetService<IRepository>();
        }

        public async Task Init()
        {
            highScoreTable = correctGuesses = 0;
            NumGuesses = $"Wrong Guesses : {guesses}";
            if (DifficultLevel == Difficulty.Hard)
                Numguess = 5;
            else
                Numguess = DifficultLevel == Difficulty.Easy ? 20 : 10;
            DifficultGuesses = $"{Numguess} guesses only!!!!";
            ShuffleTiles();
            HighScores = (await repository.GetList<HighScoreModel>(10)).ToObservable();
        }

        async Task PlayAudio(string name)
        {
            AudioManager.Current.CreatePlayer(await FileSystem.OpenAppPackageFileAsync($"{name}.wav")).Play();
        }

        async Task CheckHiScore()
        {
            // find range
            var max = HighScores.Max(t => t.Score);
            var min = HighScores.Min(t => t.Score);

            if (highScoreTable > min)
            {
                if (highScoreTable > max)
                {
                    HighScores.Insert(0, new HighScoreModel { Id = Guid.NewGuid(), Entered = DateTime.Now, Name = "The champ", Score = highScoreTable, Difficulty = (int)DifficultLevel });
                    HighScores.Remove(HighScores.LastOrDefault());
                    await repository.DeleteList(HighScores.ToList());
                    await repository.SaveListData(HighScores.ToList());
                    return;
                }

                // find the position in the table
                var upper = HighScores.Where(t => t.Score >= highScoreTable).Min();
                var lower = HighScores.Where(t => t.Score <= highScoreTable).Max();
                HighScores.Insert(upper.Score, new HighScoreModel { Id = Guid.NewGuid(), Entered = DateTime.Now, Name = "The contender", Score = highScoreTable, Difficulty = (int)DifficultLevel });

                HighScores.Remove(HighScores.LastOrDefault());

                await repository.DeleteList(HighScores.ToList());
                await repository.SaveListData(HighScores.ToList());
            }
        }

        void ShuffleTiles()
        {
            var baseTiles = new ObservableCollection<string>
            {
                "cups", "devil", "knight", "lovers", "magician", "pentacles", "queen", "swords",
                "cups", "devil", "knight", "lovers", "magician", "pentacles", "queen", "swords"
            };

            Tiles = baseTiles.OrderBy(_ => random.Next()).ToList().ToObservable();
        }

        void ShowTile(int tile, bool imagetwo = false)
        {
            if (imagetwo)
                ImageTwo = $"{Tiles[tile]}.png";
            else
                ImageOne = $"{Tiles[tile]}.png";
        }
    }
}
