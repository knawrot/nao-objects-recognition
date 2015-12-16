package pl.edu.agh.naoapplication.learning;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

public class DetectionTrainer {
	private static final Logger logger = Logger.getLogger(DetectionTrainer.class);
	private static final String TMP_NEGATIVE_FILE = "tmp_negative.dat";
	private static final String TMP_POSITIVE_FILE = "tmp_positive.dat";
	private static final String TMP_VECTOR_FILE = "tmp_vector.vec";
	private String positiveImagesDir;
	private String[] positiveImagesFileNames;
	private String negativeImagesDir;
	private String[] negativeImagesFileNames;
	
	public DetectionTrainer(String positiveImagesDir, String negativeImagesDir) {
		if ( !(new File(positiveImagesDir)).isDirectory() ||
			 !(new File(negativeImagesDir)).isDirectory() )
			throw new IllegalArgumentException("Provided strings must"
											+ " point to an existing directory");
		this.positiveImagesDir = positiveImagesDir;
		this.negativeImagesDir = negativeImagesDir;
		this.positiveImagesFileNames = (new File(positiveImagesDir)).list();
		this.negativeImagesFileNames = (new File(negativeImagesDir)).list();
	}
	
	// TODO: refactor each try catches with methods throwing exception 
	// and handle them all at once
	public void createTrainingSamples() {
		Path tmpPositiveFile = Paths.get(TMP_POSITIVE_FILE);
		List<String> positiveFileFormatter = formatLines(positiveImagesDir,
														positiveImagesFileNames);
		Path tmpNegativeFile = Paths.get(TMP_NEGATIVE_FILE);
		List<String> negativeFileFormatter = formatLines(negativeImagesDir,
														negativeImagesFileNames);
		
		try {
			Files.write(tmpPositiveFile, positiveFileFormatter, 
						StandardOpenOption.CREATE);
			Files.write(tmpNegativeFile, negativeFileFormatter, 
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
												" -w 48" +
												" -h 48" +
												" -num " + positiveFileFormatter.size())
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
	}

	private List<String> formatLines(String realtiveDirectory, String[] fileNames) {
		List<String> list = new ArrayList<String>(); 
		for (String fileName : fileNames) {
			list.add(String.format("%s/%s 1 0 0 50 50", realtiveDirectory, fileName));
		}
		return list;
	}

}
