package pl.edu.agh.naoapplication.learning;

import org.apache.log4j.BasicConfigurator;

public class DetectionTrainerRunner {
	
	public static void main(String[] args) {
		BasicConfigurator.configure();
		String pathToImagesDir = "resourcers/images";
		DetectionTrainer myLearner = new DetectionTrainer(pathToImagesDir, pathToImagesDir);
		myLearner.createTrainingSamples();
	}

}
