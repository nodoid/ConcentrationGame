﻿using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Concentration.Enums;
using Concentration.Helpers;
using Plugin.Maui.Audio;
using System.Collections.ObjectModel;

namespace Concentration.ViewModels
{
    public partial class GameViewModel : BaseViewModel
    {
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

        int guesses { get; set; }
        [ObservableProperty]
        int tileOne  = -1;
        [ObservableProperty]
        int tileTwo  = -1;

        [ObservableProperty]
        int numguess = 0;

        Random random = new Random();

        [RelayCommand]
        public async Task ButtonPressed()
        {
            await PlayAudio("scream");
            Tiles.Clear();
            ResetBoard = true;
        }

        [RelayCommand]
        public async Task TileSelected(string tile)
        {
            await PlayAudio("slice");
            if (TileOne == -1)
            {
                TileOne = Convert.ToInt32(tile);
                ShowTile(TileOne);
            }
            else
            {
                TileTwo = Convert.ToInt32(tile);
                ShowTile(TileTwo, true);
                guesses++;
            }
            if (TileTwo != -1)
            {
                if (Tiles[TileOne].Equals(Tiles[TileTwo]))
                {
                    Score++;
                }
                else
                {
                    NumGuesses = $"Wrong Guesses : {guesses}";
                }
            }
            if (guesses == Numguess)
            {
                ShowButton = true;
                if (Score != 8)
                {
                    await PlayAudio("creepyGirl");
                }
            }
            if (TileOne != -1 && TileTwo != -1)
            {
                TileOne = TileTwo = -1;
            }
        }

        public void Init()
        {
            NumGuesses = $"Wrong Guesses : {guesses}";
            Numguess = DifficultLevel == Difficulty.Easy ? 10 : 5;
            DifficultGuesses = $"{Numguess} guesses only!!!!";
            ShuffleTiles();
        }

        async Task PlayAudio(string name)
        {
            AudioManager.Current.CreatePlayer(await FileSystem.OpenAppPackageFileAsync($"{name}.wav")).Play();
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