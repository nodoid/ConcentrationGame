namespace Concentration.Interfaces
{
    public interface IRepository
    {
        Task SaveData<T>(T toStore);

        Task SaveListData<T>(List<T> toStore);

        Task<List<T>> GetList<T>(int top = 0) where T : class, new();

        Task<List<T>> GetList<T, TU>(string para, TU val, int top = 0) where T : class, new();

        Task<T?> GetData<T>() where T : class, new();

        Task<T?> GetData<T, TU>(string para, TU val) where T : class, new();

        Task<T?> GetData<T, TU, TV>(string para1, TU val1, string para2, TV val2) where T : class, new();

        Task Delete<T>(T stored);

        Task DeleteList<T>(List<T> list);

        Task<int> GetID<T>() where T : class, new();

        Task<int> Count<T>() where T : class, new();

        Task<int> Count<T, U>(string p, U val) where T : class, new();

        Task DeleteAll();
    }
}
