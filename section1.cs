using System;
using System.Collections.Concurrent;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
 
class Program
{
    // Simulated sensor data
    public class SensorData
    {
        public int SensorId { get; set; }
        public double Temperature { get; set; }
        public double Humidity { get; set; }
        public DateTime Timestamp { get; set; }
    }
 
    static async Task Main(string[] args)
    {
        // Simulating IoT sensors
        int sensorCount = 2;
        ConcurrentBag<SensorData> sensorDataBag = new();
 
        // Simulate data collection from sensors
        var cts = new CancellationTokenSource();
        var token = cts.Token;
 
        Console.WriteLine("Starting IoT Sensor Data Aggregation... Press Enter to stop.");
        var sensorTasks = Enumerable.Range(1, sensorCount)
            .Select(sensorId => SimulateSensor(sensorId, sensorDataBag, token))
            .ToList();
 
        // Process data while sensors are running
        var processingTask = Task.Run(() => ProcessSensorData(sensorDataBag, token));
 
        // Wait for user to stop the simulation
        Console.ReadLine();
        cts.Cancel();
 
        await Task.WhenAll(sensorTasks);
        await processingTask;
 
        Console.WriteLine("Aggregation stopped. Final data:");
        Console.WriteLine($"Total records collected: {sensorDataBag.Count}");
    }
 
    // Simulates a single sensor generating data
    static async Task SimulateSensor(int sensorId, ConcurrentBag<SensorData> dataBag, CancellationToken token)
    {
        Random random = new(sensorId);
 
        while (!token.IsCancellationRequested)
        {
            var data = new SensorData
            {
                SensorId = sensorId,
                Temperature = Math.Round(random.NextDouble() * 40, 2),
                Humidity = Math.Round(random.NextDouble() * 100, 2),
                Timestamp = DateTime.UtcNow
            };
 
            dataBag.Add(data);
            await Task.Delay(random.Next(500, 10000)); // Simulating varying sensor intervals
        }
    }
 
    // Processes and aggregates data from the sensorDataBag
    static void ProcessSensorData(ConcurrentBag<SensorData> dataBag, CancellationToken token)
    {
        while (!token.IsCancellationRequested)
        {
            if (!dataBag.IsEmpty)
            {
                var dataSnapshot = dataBag.ToList(); // Take a snapshot
                dataBag.Clear(); // Clear the bag for new data
 
                // Aggregate data
                var averageTemperature = dataSnapshot.Average(d => d.Temperature);
                var averageHumidity = dataSnapshot.Average(d => d.Humidity);
 
                Console.WriteLine($"Processed {dataSnapshot.Count} records:");
                Console.WriteLine($"Average Temperature: {averageTemperature:F2}°C");
                Console.WriteLine($"Average Humidity: {averageHumidity:F2}%");
                Console.WriteLine("-----------------------------------");
            }
 
            Thread.Sleep(1000); // Pause for next batch
        }
    }
}