using Concentration.Enums;

namespace Concentration.Converters
{
    public class DifficultyToStringConverter : IValueConverter
    {
        public object Convert(object? value, Type targetType, object? parameter, System.Globalization.CultureInfo culture)
        {
            var prop = value is Difficulty d ? d : Difficulty.Medium;

            return prop == Difficulty.Hard ? "Hard" : (prop == Difficulty.Easy ? "Easy" : "Medium");
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, System.Globalization.CultureInfo culture) => string.Empty;
    }
}
