using CommunityToolkit.Mvvm.ComponentModel;
using Concentration.Enums;

namespace Concentration.ViewModels
{
    public partial class BaseViewModel : ObservableObject
    {
        [ObservableProperty]
        Difficulty difficultLevel;
    }
}
