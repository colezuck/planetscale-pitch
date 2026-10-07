# Intercom TeachBack evidence and art

Reviewed October 6, 2026. Primary source: [Intercom engineering report, March 11, 2025](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure-lessons-and-progress/). The [PlanetScale case-study listing](https://planetscale.com/case-studies/intercom) points to this customer story.

Intercom’s migration was Aurora MySQL/custom sharding → PlanetScale Vitess/EBS → Metal. The Metal-specific comparison is against the intermediate EBS setup, not a direct Aurora Postgres test. Peak-load IOPS saturation degraded the Inbox; adding capacity and moving to io2 was the immediate workaround. The reported Metal outcomes are faster and more consistent conversation loading, 60%+ lower database cost versus previous EBS io2, and no availability issues caused by migrated databases at report time. Customer-downtime-free maintenance was a Vitess failover result. Do not promise perpetual availability. The separate 90%+ query gain involved materialized-view rewrites, not Metal alone.

The visible static slide reuses the original hourly database cost image and official Intercom logo already in the Postgres pitch; both files are copied unchanged into TeachBack assets. The image has no numeric axis labels. The 60%+ callout comes from the article text, not inferred chart values. No cost curve, time markers or new numeric axes were reconstructed.

Original image URL: https://blog.intercomassets.com/blog/wp-content/uploads/2025/03/Evolving-Intercoms-Database-Infrastructure-Lessons-and-Progress-1-scaled.jpg

Local image: `decks/teach-back/assets/intercom-original-cost-full.jpg`.
SHA-256: fb69679f88c3c11c56816504b807103897667ba2a81e7884d0035774a3e7a467.

Brand/source rights remain with Intercom. Reuse here is for the requested interview presentation. Artwork and source claim scope are checked separately from the original pitch’s speaking notes.

## Focused slide revision — October 6, 2026

Removed the three generic outcome headings and the availability/maintenance text from the visible slide. The one customer-impact line now emphasizes consistent Inbox loading at peak load, supported by the Metal section. Availability and maintenance remain in the notes with report-date and Vitess attribution. The report’s mention of its largest customers generating the most data belongs to the materialized-view query rewrite result; it is not a distinct Metal outcome. The high-volume-team sentence in the notes explains business relevance rather than claiming a measured customer-segment result.
