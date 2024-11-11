using System.Collections.ObjectModel;

namespace Concentration.Helpers
{
    public static class ToObservableCollection
    {
        public static ObservableCollection<T> ToObservable<T>(this List<T> collection) => 
            new ObservableCollection<T>(collection as IEnumerable<T>);
    }
}
