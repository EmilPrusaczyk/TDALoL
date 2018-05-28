import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.barcodes.Interval;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.streams.impl.ExplicitSimplexStream;
import edu.stanford.math.plex4.streams.impl.VietorisRipsStream;
import edu.stanford.math.plex4.visualization.BarcodeVisualizer;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public void jeden() {
        ExplicitSimplexStream stream = Plex4.createExplicitSimplexStream();
        stream.addVertex(0);
        stream.addVertex(1);
        stream.addVertex(2);
        stream.addElement(new int[] {0, 1});
        stream.addElement(new int[] {0, 2});
        stream.addElement(new int[] {1, 2});

        int numSimplices = stream.getSize();
        //System.out.println(numSimplices);

        AbstractPersistenceAlgorithm persistence = Plex4.getModularSimplicialAlgorithm(3, 2);
        BarcodeCollection intervals = persistence.computeIntervals(stream);
        //System.out.println(intervals.toString());
    }

    public static BufferedImage draw(double[][] pointCloud, String teamName, int dim, int f) {
        BufferedImage img = null;
        VietorisRipsStream stream = Plex4.createVietorisRipsStream(pointCloud, 3, f, 1000);
        AbstractPersistenceAlgorithm persistence = Plex4.getModularSimplicialAlgorithm(3, 2);
        BarcodeCollection intervals = persistence.computeIntervals(stream);
        //System.out.println(intervals.toString());

        List<Interval<Double>> list = intervals.getIntervalsAtDimension(dim);
        for(Interval<Double> interval : list) {
            //System.out.println(interval.toString());
        }
        try {
            img = BarcodeVisualizer.drawBarcode(list, teamName + "(dimension: " + dim + ")", f);
            File outputfile = new File(teamName + "_dim" + dim + ".png");
            ImageIO.write(img, "png", outputfile);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return img;
    }

    static void regionBarcodes(int f) {
        List<String> regionNames = new ArrayList<>();

        BufferedReader br = null;
        FileReader fr = null;

        try {
            fr = new FileReader("regions");
            br = new BufferedReader(fr);

            String line;

            while((line = br.readLine()) != null) {
                regionNames.add(line.split(",")[0]);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            closeReaders(br, fr);
        }

        for(String regionName : regionNames) {
            Team region = new Team(regionName);
            populateTeam(regionName, region);

            int n = region.players.size();
            double[][] points = new double[n][];
            for(int i = 0; i < n; i++) {
                points[i] = region.players.get(i).stats;
            }

            draw(points, regionName, 0, f);
            draw(points, regionName, 1, f);
        }
    }

    private static void populateTeam(String regionName, Team region) {
        FileReader fr;
        BufferedReader br;
        try {
            fr = new FileReader("teamstats/" + regionName);
            br = new BufferedReader(fr);

            String line;

            while((line = br.readLine()) != null) {
                String[] values = line.split(",");
                if(values[0].equals("Player")) {
                    continue;
                }

                double[] stats = new double[values.length - 1];
                for(int i = 1; i < values.length; i++) {
                    stats[i-1] = Double.parseDouble(values[i]);
                }

                region.addPlayer(new Player(values[0], stats));
            }

            for(Player player : region.players) {
                //System.out.println(player.name);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void closeReaders(BufferedReader br, FileReader fr) {
        try {
            if(br != null) {
                br.close();
            }
            if(fr != null) {
                fr.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void teamBarcodes(int f) {
        List<String> teamNames = new ArrayList<>();

        BufferedReader br = null;
        FileReader fr = null;

        try {
            fr = new FileReader("teams");
            br = new BufferedReader(fr);

            String line;

            while((line = br.readLine()) != null) {
                teamNames.add(line.split(",")[0]);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            closeReaders(br, fr);
        }

        for(String teamName : teamNames) {
            Team team = new Team(teamName);
            populateTeam(teamName, team);

            double[][] points = new double[5][];
            for(int i = 0; i < 5; i++) {
                points[i] = team.players.get(i).stats;
            }

            draw(points, teamName, 0, f);
            draw(points, teamName, 1, f);
        }
    }

    public static void main(String[] args) {
        teamBarcodes(700);
        regionBarcodes(100);
    }
}

class Team {
    public String name;
    public List<Player> players;

    Team(String name) {
        this.name = name;
        this.players = new ArrayList<>();
    }

    public void addPlayer(Player player) {
        players.add(player);
    }
}

class Player {
    public String name;
    public double[] stats;

    Player(String name, double[] stats) {
        this.name = name;
        this.stats = stats;
    }
}