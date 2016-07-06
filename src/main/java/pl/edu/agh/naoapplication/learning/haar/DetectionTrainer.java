package pl.edu.agh.naoapplication.learning.haar;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import pl.edu.agh.naoapplication.learning.Configuration;

public class DetectionTrainer {
	private static final Logger logger = Logger.getLogger(DetectionTrainer.class);
	private static final String TMP_NEGATIVE_FILE = "tmp_negative.dat";
	private static final String TMP_POSITIVE_FILE = "tmp_positive.dat";
	private static final String TMP_VECTOR_FILE = "tmp_vector.vec";
	
	
	// TODO: refactor each try catches with methods throwing exception 
	// and handle them all at once
	public static void createTrainingSamples(String positiveImagesDir, 
											 String negativeImagesDir) {
		checkArguments(positiveImagesDir,negativeImagesDir);
		
//		String[] positiveImagesFileNames = (new File(positiveImagesDir)).list();
		String[] negativeImagesFileNames = (new File(negativeImagesDir)).list();
//		List<String> positiveFileFormatter = formatLines(positiveImagesDir,
//														positiveImagesFileNames,
//														true);
		List<String> negativeFileFormatter = formatLines(negativeImagesDir,
														negativeImagesFileNames,
														false);
		
		try {
//			Files.write(Paths.get(TMP_POSITIVE_FILE), positiveFileFormatter, 
//						StandardOpenOption.CREATE);
			Files.write(Paths.get(TMP_NEGATIVE_FILE), negativeFileFormatter, 
						StandardOpenOption.CREATE);
		} catch (IOException e1) {
			logger.error("Error during creating temporary files: ", e1);
			return;
		}
		logger.info("Created temporary input files.");

		try {
			Process createSamplesProcess = new ProcessBuilder(
											"cmd", "/c",
											Configuration.CREATE_SAMPLES_PROGRAM +
											" -info " + TMP_POSITIVE_FILE +
											" -vec " + TMP_VECTOR_FILE +
											" -w 20" +
											" -h 20" +
											" -num 105")
											//.inheritIO() - redirect outs for log
											.start();
			int exitCode = createSamplesProcess.waitFor(); 
			if (exitCode != 0) {
				logger.error("opencv_createsamples failed to complete process"
						+ " and returned exitcode: " + exitCode);
			}
		} catch (IOException | InterruptedException e) {
			logger.error("Error during running samples: ", e);
			return;
		}
		logger.info("Created temporary vector file.");
		
		try {
			Process trainCascadeProcess = new ProcessBuilder(
											"cmd", "/c",
											Configuration.TRAIN_CASCADE_PROGRAM +
											" -data data" +
											" -vec " + TMP_VECTOR_FILE +
											" -bg " + TMP_NEGATIVE_FILE +
											" -baseFormatSave" + 
											" -numPos 105" + 
											" -numNeg " + negativeFileFormatter.size() +
											" -numStages 20" +
											" -nsplits 2" +
											" -minhitrate 0.999" +
											" -maxfalsealarm 0.5" +
//											" -nonsym" + - causes crashes of app
//											" -mode ALL" +
											" -w 20" +
											" -h 20")
											.inheritIO() // - redirect outs for log
											.start();
			int exitCode = trainCascadeProcess.waitFor(); 
			if (exitCode != 0) {
				logger.error("opencv_traincascade failed to complete process"
						+ " and returned exitcode: " + exitCode);
			}
		} catch (IOException | InterruptedException e) {
			logger.error("Error during training classifier: ", e);
			return;
		}
		logger.info("Created HAAR classifier in /data directory.");
	}

	private static void checkArguments(String positiveImagesDir, 
									   String negativeImagesDir) {
		if ( !(new File(positiveImagesDir)).isDirectory() ||
			 !(new File(negativeImagesDir)).isDirectory() )
					throw new IllegalArgumentException("Provided strings must"
												+ " point to an existing directory");
	}

	private static List<String> formatLines(String realtiveDirectory, 
											String[] fileNames, 
											boolean positiveSample) {
		List<String> list = new ArrayList<String>(); 
		for (String fileName : fileNames) {
			if (positiveSample)
				list.add(String.format("%s/%s 1 0 0 512 409", realtiveDirectory, 
										fileName));
			else
				list.add(String.format("%s/%s", realtiveDirectory, fileName));
		}
		return list;
	}

}
