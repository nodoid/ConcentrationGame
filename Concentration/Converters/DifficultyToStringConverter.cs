using Concentration.Enums;

namespace Concentration.Converters
{
    public class DifficultyToStringConverter : IValueConverter
    {
        public object Convert(object? value, Type targetType, object? parameter, System.Globalization.CultureInfo culture)
        {
            // high scores store the difficulty as an int
            var prop = value switch { Difficulty d => d, int i => (Difficulty)i, _ => Difficulty.Medium };

            return prop == Difficulty.Hard ? "Hard" : (prop == Difficulty.Easy ? "Easy" : "Medium");
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, System.Globalization.CultureInfo culture) => string.Empty;
    }
}
