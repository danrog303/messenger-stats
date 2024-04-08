package com.github.danrog303.messengerstats.services.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

@Configuration
public class SpringSecurityConfig {

    @Bean
    public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        SecurityWebFilterChain build = http
                .authorizeExchange((authorize) -> authorize
                        .anyExchange().permitAll()
                ).csrf((csrf) -> csrf.disable()).build();
        return
                build;
    }
}
