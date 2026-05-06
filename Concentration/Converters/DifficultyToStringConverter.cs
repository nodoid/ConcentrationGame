using Concentration.Enums;
using System;
using System.Collections.Generic;
using System.Text;

namespace Concentration.Converters
{
    public class DifficultyToStringConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            var prop = (Difficulty)parameter;

            return prop == Difficulty.Hard ? "Hard" : (prop == Difficulty.Easy ? "Easy" : "Medium");
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture) => string.Empty;
    }
}
