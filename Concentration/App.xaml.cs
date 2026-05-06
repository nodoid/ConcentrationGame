using Concentration.Database;
using Concentration.Interfaces;
using SQLite;

namespace Concentration
{
    public partial class App : Application
    {
        public static IServiceProvider Service { get; private set; }
        public static App Self { get; private set; }
        public static SQLiteAsyncConnection SQLConnection { get; set; }

        public App()
        {
            App.Self = this;

            Service = Startup.Init();
            InitializeComponent();
            
            SetupSQLiteConnection();

            // create SQLite repositiory class
            new SqLiteRepository();
        }

        // Updated to avoid direct dependency on IActivationState API surface
        // which has changed in newer MAUI/.NET versions.
        protected override Window CreateWindow() => new Window(new AppShell());

        void SetupSQLiteConnection()
        {
            var path = Environment.GetFolderPath(Environment.SpecialFolder.Personal);
            path = Path.Combine(path, "conchiscore.db");

            try
            {
                App.SQLConnection = new SQLiteAsyncConnection(path, SQLiteOpenFlags.ReadWrite | SQLiteOpenFlags.Create);
            }
            catch (Exception ex)
            {
#if DEBUG
                Console.WriteLine(
                    $"Connection could  not be made : ex.Message = {ex.Message} - inner = {ex.InnerException?.Message}");
#endif
            }
        }
    }
}
