package com.github.danrog303.messengerstats.domain.stats;

import com.github.danrog303.messengerstats.domain.event.ReactiveEvent;
import com.github.danrog303.messengerstats.services.zip.ArchiveService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.nio.file.Path;

@Service
@RequiredArgsConstructor
public class ChatStatPathHandler {
    @Value("${messengerstats.filecontainer}")
    private String workDirPath;

    @Value("${messengerstats.stats-service-url}")
    private String statsServicePath;

    private final WebClient webClient;
    private final ArchiveService archiveService;

    public Mono<ServerResponse> getMessengerStatistics(ServerRequest req) {
        String fileKey = req.pathVariable("dataFileKey");
        String sourcePath = Path.of(workDirPath, fileKey + "." + "zip").toString();
        String destinationPath = Path.of(workDirPath, "unpacked_" + fileKey).toString();
        String statsServiceEndpoint = "%s/stats/%s".formatted(statsServicePath, "unpacked_"+fileKey);

        Flux<?> re = Flux.concat(
            Mono.just(ReactiveEvent.eventInfoOf("unzip-start")),
            archiveService.unzip(sourcePath, destinationPath),
            Mono.just(ReactiveEvent.eventInfoOf("unzip-finish")),
            Mono.just(ReactiveEvent.eventInfoOf("stats-read-start")),
            webClient.get().uri(statsServiceEndpoint).retrieve().bodyToFlux(ChatStatEntry.class).map(ReactiveEvent::dataPortionOf),
            Mono.just(ReactiveEvent.eventInfoOf("stats-read-finish"))
        );

        return ServerResponse.ok().contentType(MediaType.TEXT_EVENT_STREAM).body(re, ReactiveEvent.class);
    }
}
