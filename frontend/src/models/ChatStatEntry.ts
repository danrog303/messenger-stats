export default interface ChatStatsEntry {
    type: string;
    metrics: Record<string, number>;
}