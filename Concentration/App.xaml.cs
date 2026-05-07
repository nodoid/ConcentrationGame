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
            _ = new SqLiteRepository();
        }

        protected override Window CreateWindow(IActivationState? activationState) => new Window(new AppShell());

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
