using SQLite;

namespace Concentration.Models;

public class HighScoreModel
{
    [PrimaryKey]
    public Guid Id { get; set; }
    [MaxLength(24)]
    public string Name { get; set; } = "";
    public int Score { get; set; }
    public DateTime Entered { get; set; } = DateTime.Now;
    public int Difficulty { get; set; }
}