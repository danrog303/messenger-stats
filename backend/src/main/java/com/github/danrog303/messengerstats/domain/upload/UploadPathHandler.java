package com.github.danrog303.messengerstats.domain.upload;

import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.RandomStringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.codec.multipart.FilePart;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyExtractors;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class UploadPathHandler {

    @Value("${messengerstats.filecontainer}")
    private String uploadPath;

    public Mono<ServerResponse> fileUpload(ServerRequest request){
        return request.body(BodyExtractors.toMultipartData())
                .flatMap(parts -> {
                    FilePart filePart = (FilePart) parts.toSingleValueMap().get("file");
                    String fileExtension = FilenameUtils.getExtension(filePart.filename());
                    String fileName = RandomStringUtils.randomAlphanumeric(32);
                    Path filePath = Paths.get(uploadPath, fileName + "." + fileExtension);
                    return filePart.transferTo(filePath).then(ServerResponse.ok().bodyValue(fileName));
                });
    }
}
