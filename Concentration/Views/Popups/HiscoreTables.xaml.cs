namespace Concentration.Views.Popups;

public partial class HiscoreTables : Mopups.Pages.PopupPage
{
    public HiscoreTables()
    {
        InitializeComponent();
    }

    protected override void OnAppearing()
    {
        base.OnAppearing();
        Task.Run(async () => await ViewModel.Init());
    }

    protected override bool OnBackButtonPressed()
    {
        return base.OnBackButtonPressed();
    }

    protected override bool OnBackgroundClicked()
    {
        return base.OnBackgroundClicked();
    }
}