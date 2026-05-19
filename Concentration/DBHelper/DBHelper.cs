using System.Diagnostics;
using Concentration.Interfaces;
using Concentration.Models;
using SQLite;

namespace Concentration.Database
{
    public class SqLiteRepository : IRepository
    {
        readonly SQLiteAsyncConnection connection;

        public SqLiteRepository()
        {
            connection = App.SQLConnection;

            Task.Run(async() => await CreateTables());
        }

        public async Task  SaveData<T>(T toStore)
        {
            try
            {
                await connection.InsertOrReplaceAsync(toStore);
            }
            catch (Exception ex)
            {
#if DEBUG
                Debug.WriteLine(ex.Message);
#endif
            }
        }

        public async Task SaveListData<T>(List<T> toStore)
        {
            try
            {
                foreach (var ts in toStore)
                    await connection.InsertOrReplaceAsync(ts);
            }
            catch (Exception ex)
            {
#if DEBUG
                Debug.WriteLine($"{ex.Message}--{ex.InnerException?.Message}");
#endif
            }
        }

        public async Task<int> Count<T>() where T : class, new()
        {
            return (await GetList<T>()).Count;
        }

        public async Task<List<T>> GetList<T>(int top = 0) where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0}", GetName(typeof(T).ToString()));
            try
            {
                var list = await connection.QueryAsync<T>(sql, string.Empty);
                if (list.Count != 0)
                {
                    if (top != 0)
                    {
                        list = list.Take(top).ToList();
                    }
                }

                return list;
            }
            catch(Exception ex)
            { 
                Debug.WriteLine(ex.Message); 
                return new List<T>();
            }
        }

        public async Task<List<T>> GetList<T, TU>(string para, TU val, int top = 0) where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0} WHERE {1}=?", GetName(typeof(T).ToString()), para);
            var list = await connection.QueryAsync<T>(sql, val);
            if (list.Count != 0)
            {
                if (top != 0)
                {
                    list = list.Take(top).ToList();
                }
            }

            return list;
        }

        public async Task<T?> GetData<T>() where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0}", GetName(typeof(T).ToString()));
            var list = await connection.QueryAsync<T>(sql, string.Empty);
            return list != null ? list.FirstOrDefault() : default;
        }

        public async Task<T?> GetData<T, TU>(string para, TU val) where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0} WHERE {1}=?", GetName(typeof(T).ToString()), para);
            var list = await connection.QueryAsync<T>(sql, val);
            return list != null ? list.FirstOrDefault() : default;
        }

        public async Task DeleteAll()
        {
            try
            {
                await connection.DeleteAllAsync<HighScoreModel>();
            }
            catch (Exception ex)
            {
#if DEBUG
                Debug.WriteLine($"{ex.Message}--{ex.InnerException?.Message}");
#endif
            }

        }

        public async Task Delete<T>(T stored)
        {
            try
            {
                await connection.DeleteAsync(stored);
            }
            catch (Exception ex)
            {
#if DEBUG
                Debug.WriteLine($"{ex.Message}--{ex.InnerException?.Message}");
#endif
            }
        }

        public async Task DeleteList<T>(List<T> list)
        {
            try
            {
                foreach (var l in list)
                    await connection.DeleteAsync(l);
            }
            catch (Exception ex)
            {
#if DEBUG
                Debug.WriteLine($"{ex.Message}--{ex.InnerException?.Message}");
#endif
            }
        }

        public async Task<T?> GetData<T, TU, TV>(string para1, TU val1, string para2, TV val2) where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0} WHERE {1}=? AND {2}=?", GetName(typeof(T).ToString()), para1, para2);
            var list = await connection.QueryAsync<T>(sql, val1, val2);
            return list != null ? list.FirstOrDefault() : default;
        }

        public async Task<int> GetID<T>() where T : class, new()
        {
            string sql = string.Format("SELECT last_insert_rowid() FROM {0}", GetName(typeof(T).ToString()));
            var id = await connection.ExecuteScalarAsync<int>(sql, string.Empty);
            return id;
        }

        async Task CreateTables()
        {
            try
            {
                await connection.CreateTableAsync<HighScoreModel>();
            }
            catch(Exception ex)
            {
                Console.WriteLine($"Exception thrown - {ex.Message}--{ex.InnerException?.Message}");
            }
        }

        string GetName(string name)
        {
            var list = name.Split('.').ToList();
            if (list.Count == 1)
            {
                return list[0];
            }

            return list[^1];
        }

        public async Task<int> Count<T, U>(string p, U val) where T : class, new()
        {
            var sql = string.Format("SELECT * FROM {0} WHERE {1}={2}", GetName(typeof(T).ToString()), p, val);
            var list = await connection.QueryAsync<T>(sql, string.Empty);
            return list.Count;

        }
    }
}
