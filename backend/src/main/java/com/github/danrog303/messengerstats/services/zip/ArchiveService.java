package com.github.danrog303.messengerstats.services.zip;

import net.lingala.zip4j.core.ZipFile;
import net.lingala.zip4j.exception.ZipException;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;


@Service
public class ArchiveService {
    public Mono<Void> unzip(String zipFilePath, String destination) {
        return Mono.fromRunnable(() -> {
            try {
                ZipFile zipFile = new ZipFile(zipFilePath);
                zipFile.extractAll(destination);
            } catch (ZipException e) {
                throw new RuntimeException("Failed to unzip file", e);
            }
        });
    }
}
