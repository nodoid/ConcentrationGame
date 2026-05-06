using CommunityToolkit.Mvvm.Messaging;
using Concentration.Database;
using Concentration.Interfaces;
using Concentration.ViewModels;

namespace Concentration.Helpers
{
    public static class  InjectionContainer
    {
        public static IServiceCollection ConfigureServices(this IServiceCollection services)
        {
            var i = new ServiceCollection();

            i.AddSingleton<IRepository, SqLiteRepository>().
            AddSingleton<IMessenger>(WeakReferenceMessenger.Default);

            services = i;

            return services;
        }

        public static IServiceCollection ConfigureViewModels(this IServiceCollection services)
        {
            services.AddTransient<BaseViewModel>();
            services.AddScoped<GameViewModel>();
            services.AddScoped<StartupViewModel>();

            return services;
        }

    }
}
