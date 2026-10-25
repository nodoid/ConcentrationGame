namespace Concentration.Views
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();
            Task.Run(async () => await viewModel.Init());
#if SCREENSHOTS
            Task.Run(async () => await Helpers.ScreenshotDriver.OnMainPage(viewModel));
#endif
        }
    }
}
