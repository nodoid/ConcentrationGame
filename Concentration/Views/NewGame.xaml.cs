namespace Concentration.Views;

public partial class NewGame : ContentPage
{
    public NewGame()
    {
        InitializeComponent();
    }

    protected override void OnAppearing()
    {
        base.OnAppearing();
        viewModel.Init();
        viewModel.PropertyChanged += ViewModel_PropertyChanged;
    }

    void ViewModel_PropertyChanged(object? sender, System.ComponentModel.PropertyChangedEventArgs e)
    {
        switch (e.PropertyName)
        {
            case "TileOne":
                ShowTile(viewModel.TileOne);
                break;
            case "TileTwo":
                ShowTile(viewModel.TileTwo, true);
                break;
            case "ResetBoard":
                if (viewModel.ResetBoard)
                    ResetBoard();
                break;
        }
    }

    void ShowTile(int tile, bool istwo = false)
    {
        var src = istwo ? viewModel.ImageTwo : viewModel.ImageOne;
        switch (tile)
        {
            case 0:
                tile0.Source = src;
                break;
            case 1:
                tile1.Source = src;
                break;
            case 2:
                tile2.Source = src;
                break;
            case 3:
                tile3.Source = src;
                break;
            case 4:
                tile4.Source = src;
                break;
            case 5:
                tile5.Source = src;
                break;
            case 6:
                tile6.Source = src;
                break;
            case 7:
                tile7.Source = src;
                break;
            case 8:
                tile8.Source = src;
                break;
            case 9:
                tile9.Source = src;
                break;
            case 10:
                tile10.Source = src;
                break;
            case 11:
                tile11.Source = src;
                break;
            case 12:
                tile12.Source = src;
                break;
            case 13:
                tile13.Source = src;
                break;
            case 14:
                tile14.Source = src;
                break;
            case 15:
                tile15.Source = src;
                break;
        }
    }

    void ResetBoard()
    {
        tile1.Source = tile2.Source = tile3.Source = tile4.Source = tile5.Source = "back.png";
        tile6.Source = tile7.Source = tile8.Source = tile9.Source = tile10.Source = "back.png";
        tile11.Source = tile12.Source = tile13.Source = tile14.Source = tile15.Source = "back.png";
        viewModel.ResetBoard = false;
    }
}