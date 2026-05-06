using Concentration.Helpers;

namespace Concentration
{
    public class Startup 
	{
		public static IServiceProvider ServiceProvider { get; set; }

		public static IServiceProvider Init()
		{
			var provider = new ServiceCollection().
				ConfigureServices().
				ConfigureViewModels().
				BuildServiceProvider();

			ServiceProvider = provider;

			return provider;
		}
	}
}