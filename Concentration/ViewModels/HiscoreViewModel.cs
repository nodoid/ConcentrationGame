using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Concentration.Helpers;
using Concentration.Interfaces;
using Concentration.Models;
using System.Collections.ObjectModel;

namespace Concentration.ViewModels
{
    public partial class HiscoreViewModel : BaseViewModel
    {
        IRepository? repository;

        [ObservableProperty]
        ObservableCollection<HighScoreModel> highScores;

        [RelayCommand]
        public async Task CloseHighscores() => await Mopups.Services.MopupService.Instance.PopAsync();

        public HiscoreViewModel() : base()
        {
            repository = Startup.ServiceProvider.GetService<IRepository>();
        }

        public HiscoreViewModel(IRepository repo) :base()
        {
            repository = repo;
        }

        public async Task Init()
        {
            HighScores = (await repository.GetList<HighScoreModel>(10)).OrderByDescending(t=>t.Score).ToList().ToObservable();
        }
    }
}
