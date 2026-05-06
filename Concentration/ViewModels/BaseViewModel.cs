using CommunityToolkit.Mvvm.ComponentModel;
using Concentration.Enums;

namespace Concentration.ViewModels
{
    public partial class BaseViewModel : ObservableObject
    {
        static Difficulty difficultLevel;
        public Difficulty DifficultLevel
        {
            get => difficultLevel;
            set => difficultLevel = value;
        }
    }
}
