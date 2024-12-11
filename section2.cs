Parallel.For(0, 20, i =>
{
    Console.WriteLine($"Processing index {i} on thread" +
       $" {Thread.CurrentThread.ManagedThreadId}");
});

for(int i=0;i<10;i++)
{
 
    Console.WriteLine($"\nProcessing index {i} on thread" +
        $" {Thread.CurrentThread.ManagedThreadId}");
}

Task task1 = Task.Run(() => 
{  Console.WriteLine("Task 1 running");  });//Thread.Sleep(5000);
Task task2 = Task.Run(() => 
{  Console.WriteLine("Task 2 running"); Thread.Sleep(5000); });//Thread.Sleep(5000);
await Task.WhenAll(task1, task2);
Console.WriteLine("All tasks completed");


//////////////////////////////////////////

async Task<int> CalculateSquareAsync(int number)
{
    Console.WriteLine($"\nProcessing index on thread" +
        $" {Thread.CurrentThread.ManagedThreadId}");
    await Task.Delay(10000); // Simulating work
    Console.WriteLine($"\nProcessing index on thread" +
        $" {Thread.CurrentThread.ManagedThreadId}");
 
    return number * number;
 
}
 
int result = await CalculateSquareAsync(5);
Console.WriteLine($"Square: {result}");


Parallel.Invoke(
    () => Console.WriteLine("Task 1 running"),
    () => Console.WriteLine("Task 2 running"),
    () => Console.WriteLine("Task 3 running")
);

////////////////////////
///
/// 

 
var account = new BankAccount();
Parallel.For(0, 10, i => account.Deposit(10)); // Parallel deposits
Console.WriteLine($"Final balance: {account.GetBalance()}");
public class BankAccount
{
    private object _lockObj = new object();
    private int _balance;
 
    public void Deposit(int amount)
    {
        // Console.WriteLine("arrived");
        // lock (_lockObj)
        //{
        _balance += amount;
        // int temp = _balance;       // Read current balance
        //  temp += amount;             // Add amount
        //_balance = temp;
        Console.WriteLine($"Deposited {amount}, new balance is {_balance}");
        //}
        //  Console.WriteLine("\nfinised");
 
    }
    public int GetBalance()
    {
        lock (_lockObj)
        {
        return _balance;
        }
    }
}
 
 


///////////////////

Parallel.For(0, 10, i => FileLogger.Log($"Log entry {i}"));
 
public class FileLogger
{
    private static Mutex _mutex = new Mutex();
 
    public static void Log(string message)
    {
       // _mutex.WaitOne(); // Wait until it's safe to enter
        try
        {
            //Console.WriteLine("Entered");
            Console.WriteLine(message);
            using (StreamWriter sw = new StreamWriter("log.txt", true))
            {
                sw.WriteLine($"{DateTime.Now}: {message}");
            }
        }
        finally
        {
         //   _mutex.ReleaseMutex(); // Release the lock
        }
    }
}
 
 


var counter = new Counter();
Parallel.For(0, 100, i => counter.Increment()); // Parallel deposits
Console.WriteLine($"Final count: {counter.GetCount()}");
 
public class Counter
{
    private object _lockObj = new object();
    private int _count;
 
    public void Increment()
    {
     //   lock (_lockObj)
       // {
            _count++;
            //Console.WriteLine($"Final count:", _count.ToString());
        //}
    }
 
    public int GetCount()
    {
        lock (_lockObj)
        {
            return _count;
        }
    }
}