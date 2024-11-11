using Microsoft.Extensions.Logging;

namespace Concentration
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("AmaticSC-Regular.ttf", "AmaticSCRegular");
                    fonts.AddFont("AmaticSC-Bold.ttf", "AmaticSCBold");
                });

#if DEBUG
    		builder.Logging.AddDebug();
#endif

            return builder.Build();
        }
    }
}
