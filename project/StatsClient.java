// Starter code generated with Claude (Anthropic); modified by Aashira
import java.net.URI;
import java.net.http.*;

public class StatsClient {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder(URI.create("http://127.0.0.1:5000/api/stats.txt")).build();
        String body = client.send(req, HttpResponse.BodyHandlers.ofString()).body();
        System.out.printf("%-3s %-15s %8s %12s %6s%n", "#", "Player", "BPM", "Steadiness", "Hits");
        int rank = 1;
        for (String line : body.split("\n")) {
            if (!line.contains("|")) continue;
            String[] f = line.split("\\|");
            System.out.printf("%-3d %-15s %8s %11s%% %6s%n", rank++, f[0], f[1], f[2], f[3]);
        }
    }
}
