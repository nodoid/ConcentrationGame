using Concentration.Database;
using Concentration.Interfaces;
using SQLite;

namespace Concentration
{
    public partial class App : Application
    {
        public static IServiceProvider Service { get; private set; } = null!;
        public static App Self { get; private set; } = null!;
        public static SQLiteAsyncConnection SQLConnection { get; set; } = null!;

        public App()
        {
            App.Self = this;

            Service = Startup.Init();
            InitializeComponent();
            
            SetupSQLiteConnection();

            // create SQLite repositiory class
            _ = new SqLiteRepository();
        }

#if SCREENSHOTS && MACCATALYST
        // a Mac App Store screenshot size: 1440x900 (2880x1800 on a Retina display)
        protected override Window CreateWindow(IActivationState? activationState) => new Window(new AppShell())
        {
            Width = 1440, Height = 900,
            MinimumWidth = 1440, MinimumHeight = 900, MaximumWidth = 1440, MaximumHeight = 900
        };
#elif SCREENSHOTS && WINDOWS
        // the Microsoft Store screenshot size, 1920x1080, for the page below the title bar (at 100% scaling):
        // the window adds 16 pixels of border across and 8 down, and the title bar is 32 high
        protected override Window CreateWindow(IActivationState? activationState) => new Window(new AppShell())
        {
            Title = "Concentration", X = 0, Y = 0, Width = 1920 + 16, Height = 1080 + 32 + 8
        };
#elif WINDOWS
        // big enough for the whole board, but no bigger than the screen (less the taskbar), and centred;
        // the game page scrolls if the window is made smaller
        protected override Window CreateWindow(IActivationState? activationState)
        {
            var screen = DeviceDisplay.Current.MainDisplayInfo;
            var screenWidth = screen.Width / screen.Density;
            var screenHeight = screen.Height / screen.Density;
            var width = Math.Min(1000, screenWidth - 40);
            var height = Math.Min(900, screenHeight - 80);
            return new Window(new AppShell())
            {
                Title = "Concentration", Width = width, Height = height, MinimumWidth = 520, MinimumHeight = 480,
                X = (screenWidth - width) / 2, Y = Math.Max(0, (screenHeight - 48 - height) / 2)
            };
        }
#else
        protected override Window CreateWindow(IActivationState? activationState) => new Window(new AppShell());
#endif

        void SetupSQLiteConnection()
        {
            var path = Path.Combine(FileSystem.Current.AppDataDirectory, "concscore.db3");

            try
            {
                App.SQLConnection = new SQLiteAsyncConnection(path, SQLiteOpenFlags.ReadWrite | SQLiteOpenFlags.Create);
            }
            catch (Exception ex)
            {
                Console.WriteLine(
                    $"Connection could  not be made : ex.Message = {ex.Message} - inner = {ex.InnerException?.Message}");
            }
        }
    }
}
