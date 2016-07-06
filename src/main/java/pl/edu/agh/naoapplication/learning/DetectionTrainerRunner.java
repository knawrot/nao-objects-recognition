package pl.edu.agh.naoapplication.learning;

import org.apache.log4j.BasicConfigurator;

import pl.edu.agh.naoapplication.learning.haar.DetectionTrainer;

public class DetectionTrainerRunner {
	
	public static void main(String[] args) {
		BasicConfigurator.configure();
		String pathToPosImagesDir = "resourcers/images/red-ball-posset-bkp";
		String pathToNegImagesDir = "resourcers/images/red-ball-negset-bkp";
		DetectionTrainer.createTrainingSamples(pathToPosImagesDir, pathToNegImagesDir);
	}

}
