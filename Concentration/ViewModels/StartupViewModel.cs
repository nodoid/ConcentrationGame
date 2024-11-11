using CommunityToolkit.Mvvm.Input;
using Concentration.Enums;

namespace Concentration.ViewModels
{
    public partial class StartupViewModel : BaseViewModel
    {
        [RelayCommand]
        async Task SetDifficulty(string button)
        {
            DifficultLevel = button == "0" ? Difficulty.Easy : Difficulty.Hard;
            await Shell.Current.GoToAsync("//NewGame");
        }
    }
}
