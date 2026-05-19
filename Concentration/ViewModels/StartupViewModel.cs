using CommunityToolkit.Mvvm.Input;
using Concentration.Enums;
using Concentration.Interfaces;
using Concentration.Models;

namespace Concentration.ViewModels
{
    public partial class StartupViewModel : BaseViewModel
    {
        IRepository? repository;

        [RelayCommand]
        async Task SetDifficulty(string button)
        {
            switch (button)
            {
                case "0":
                    DifficultLevel = Difficulty.Easy;
                    break;
                case "1":
                    DifficultLevel = Difficulty.Medium;
                    break;
                case "2":
                    DifficultLevel = Difficulty.Hard;
                    break;

            }
            await Shell.Current.GoToAsync("//NewGame");
        }

        public StartupViewModel()
        {
            repository = App.Service.GetService<IRepository>();
        }

        public async Task Init()
        {
            var hiScores = await repository.GetList<HighScoreModel>(10);
            if (hiScores.Count <= 10) 
            {
                for (var i = hiScores.Count; i < 10; i++)
                {
                    await repository.SaveData(new HighScoreModel { Id= Guid.NewGuid(), Entered = DateTime.Now, Name = "The chump", Score = 1, Difficulty = (int)Difficulty.Easy });
                }
            }
        }
    }
}
