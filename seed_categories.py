from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category

AWARD_CATEGORIES = [
    # ============================================================
    # MUSIC & ENTERTAINMENT
    # ============================================================
    {'name': 'Best New Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-star', 'description': 'Recognizing the most promising new artist who has made a significant impact.'},
    {'name': 'Best Music Video of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-video', 'description': 'Awarded to the most creative and visually stunning music video.'},
    {'name': 'Best Collaboration of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-handshake', 'description': 'Celebrating the best musical collaboration between artists.'},
    {'name': 'Best Live Performer of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-microphone-alt', 'description': 'Recognizing the artist with the most electrifying live performances.'},
    {'name': 'Most Inspirational Musician of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-heart', 'description': 'Honoring the musician whose work inspires and uplifts others.'},
    {'name': 'Songwriter of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-pen-fancy', 'description': 'Awarded to the most talented songwriter of the year.'},
    {'name': 'Music Producer of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-headphones', 'description': 'Recognizing excellence in music production.'},
    {'name': 'Best Composition/Lyrics of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-scroll', 'description': 'Awarded for outstanding songwriting and lyrical composition.'},
    {'name': 'Best Beats/Production of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-music', 'description': 'Celebrating the best instrumental beats and music production.'},
    {'name': 'Best Worship Song of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-church', 'description': 'Honoring the most impactful worship song of the year.'},
    {'name': 'Best Gospel Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-pray', 'description': 'Recognizing excellence in gospel music.'},
    {'name': 'Best Worship Leader of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-hands-praying', 'description': 'Celebrating outstanding worship leadership.'},
    {'name': 'Best Guitarist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-guitar', 'description': 'Awarded to the most talented guitarist of the year.'},
    {'name': 'Best Keyboardist/Pianist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-piano', 'description': 'Recognizing excellence in keyboard and piano performance.'},
    {'name': 'Best Drummer of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-drum', 'description': 'Celebrating the best drummer of the year.'},
    {'name': 'Best Vocalist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-microphone', 'description': 'Awarded to the most outstanding vocalist.'},
    {'name': 'Best Afrobeat Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-globe-africa', 'description': 'Recognizing excellence in Afrobeat music.'},
    {'name': 'Best Reggae/Dancehall Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-music', 'description': 'Honoring the best reggae and dancehall artist.'},
    {'name': 'Best Hip-Hop/Rap Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-headphones', 'description': 'Celebrating the best hip-hop and rap artist.'},
    {'name': 'Best R&B/Soul Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-heart', 'description': 'Awarded to the best R&B and soul artist.'},
    {'name': 'Best Traditional/Indigenous Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-drum', 'description': 'Honoring traditional and indigenous music excellence.'},
    {'name': 'Best DJ of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-record-vinyl', 'description': 'Recognizing the best DJ of the year.'},
    {'name': 'Best Music Festival of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-ticket-alt', 'description': 'Celebrating the best music festival experience.'},
    {'name': 'Best Music Video Director of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-film', 'description': 'Awarded to the most talented music video director.'},
    {'name': 'Best Sound Engineer of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-sliders-h', 'description': 'Recognizing excellence in sound engineering.'},
    {'name': 'Best Gospel Choir of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-users', 'description': 'Honoring the best gospel choir.'},
    {'name': 'Best Praise & Worship Album of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-compact-disc', 'description': 'Awarded to the best praise and worship album.'},
    {'name': 'Best African Gospel Artist of the Year', 'group': 'Music & Entertainment', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating the best African gospel artist.'},
    
    # ============================================================
    # DANCE & PERFORMANCE
    # ============================================================
    {'name': 'Inspirational Dancer of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-dance', 'description': 'Honoring the dancer who inspires through movement.'},
    {'name': 'Best Dance Troupe of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-users', 'description': 'Celebrating the best dance troupe.'},
    {'name': 'Choreographer of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-shoe-prints', 'description': 'Awarded to the most creative choreographer.'},
    {'name': 'Best Street Dancer of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-city', 'description': 'Recognizing the best street dancer.'},
    {'name': 'Best Afro Dance Artist of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating excellence in Afro dance.'},
    {'name': 'Best Contemporary Dancer of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-arrow-right', 'description': 'Awarded to the best contemporary dancer.'},
    {'name': 'Best Traditional Dancer of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-flag', 'description': 'Honoring traditional dance excellence.'},
    {'name': 'Best Dance Instructor of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-chalkboard-teacher', 'description': 'Recognizing the best dance instructor.'},
    {'name': 'Best Dance Crew of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-users', 'description': 'Celebrating the best dance crew.'},
    {'name': 'Best Dance School/Studio of the Year', 'group': 'Dance & Performance', 'icon': 'fas fa-school', 'description': 'Awarded to the best dance school or studio.'},
    {'name': 'Best Dance Choreography for Film/TV', 'group': 'Dance & Performance', 'icon': 'fas fa-film', 'description': 'Recognizing outstanding choreography in film or television.'},
    
    # ============================================================
    # FILM & TELEVISION
    # ============================================================
    {'name': 'Best Actor of the Year (Male)', 'group': 'Film & Television', 'icon': 'fas fa-male', 'description': 'Awarded to the best male actor of the year.'},
    {'name': 'Best Actress of the Year (Female)', 'group': 'Film & Television', 'icon': 'fas fa-female', 'description': 'Awarded to the best female actress of the year.'},
    {'name': 'Best Director of the Year', 'group': 'Film & Television', 'icon': 'fas fa-video', 'description': 'Honoring the best director of the year.'},
    {'name': 'Best Screenplay Writer of the Year', 'group': 'Film & Television', 'icon': 'fas fa-pencil-alt', 'description': 'Celebrating the best screenplay writer.'},
    {'name': 'Best Film of the Year', 'group': 'Film & Television', 'icon': 'fas fa-film', 'description': 'Awarded to the best film of the year.'},
    {'name': 'Best TV Series of the Year', 'group': 'Film & Television', 'icon': 'fas fa-tv', 'description': 'Recognizing the best television series.'},
    {'name': 'Best TV Show Host of the Year', 'group': 'Film & Television', 'icon': 'fas fa-microphone', 'description': 'Awarded to the best TV show host.'},
    {'name': 'Best Documentary of the Year', 'group': 'Film & Television', 'icon': 'fas fa-file-alt', 'description': 'Honoring the best documentary film.'},
    {'name': 'Best Short Film of the Year', 'group': 'Film & Television', 'icon': 'fas fa-play-circle', 'description': 'Celebrating the best short film.'},
    {'name': 'Most Promising Filmmaker of the Year', 'group': 'Film & Television', 'icon': 'fas fa-camera', 'description': 'Recognizing emerging filmmaking talent.'},
    {'name': 'Best Film Producer of the Year', 'group': 'Film & Television', 'icon': 'fas fa-tasks', 'description': 'Awarded to the best film producer.'},
    {'name': 'Best Cinematographer of the Year', 'group': 'Film & Television', 'icon': 'fas fa-camera-retro', 'description': 'Celebrating excellence in cinematography.'},
    {'name': 'Best Sound Design in Film/TV', 'group': 'Film & Television', 'icon': 'fas fa-volume-up', 'description': 'Recognizing outstanding sound design.'},
    {'name': 'Best Costume Design in Film/TV', 'group': 'Film & Television', 'icon': 'fas fa-tshirt', 'description': 'Awarded for excellence in costume design.'},
    {'name': 'Best Animated Film of the Year', 'group': 'Film & Television', 'icon': 'fas fa-video', 'description': 'Honoring the best animated film.'},
    {'name': 'Best Independent Film of the Year', 'group': 'Film & Television', 'icon': 'fas fa-film', 'description': 'Celebrating the best independent film.'},
    
    # ============================================================
    # FASHION & DESIGN
    # ============================================================
    {'name': 'Fashion Designer of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-tshirt', 'description': 'Awarded to the best fashion designer.'},
    {'name': 'Best Emerging Designer of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-cut', 'description': 'Recognizing emerging fashion talent.'},
    {'name': 'Style Icon of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-crown', 'description': 'Honoring the most stylish personality.'},
    {'name': 'Best Fashion Model of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-walking', 'description': 'Awarded to the best fashion model.'},
    {'name': 'Best Fashion Photographer of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-camera', 'description': 'Celebrating excellence in fashion photography.'},
    {'name': 'Best African Fashion Designer of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-globe-africa', 'description': 'Honoring the best African fashion designer.'},
    {'name': 'Best Sustainable Fashion Brand of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-leaf', 'description': 'Recognizing sustainable fashion excellence.'},
    {'name': 'Best Fashion Influencer of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-share-alt', 'description': 'Awarded to the most impactful fashion influencer.'},
    {'name': 'Best Makeup Artist of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-paint-brush', 'description': 'Celebrating the best makeup artist.'},
    {'name': 'Best Hair Stylist of the Year', 'group': 'Fashion & Design', 'icon': 'fas fa-cut', 'description': 'Recognizing the best hair stylist.'},
    
    # ============================================================
    # VISUAL ARTS & CULTURE
    # ============================================================
    {'name': 'Visual Artist of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-palette', 'description': 'Awarded to the best visual artist.'},
    {'name': 'Cultural Ambassador of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-handshake', 'description': 'Honoring cultural ambassadors.'},
    {'name': 'Best Art Exhibition of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-image', 'description': 'Celebrating the best art exhibition.'},
    {'name': 'Best Digital/Graphic Artist of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-laptop', 'description': 'Recognizing digital and graphic art excellence.'},
    {'name': 'Best Traditional Artisan of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-hands', 'description': 'Honoring traditional artisans.'},
    {'name': 'Best Street Art/Urban Artist', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-city', 'description': 'Celebrating street and urban art.'},
    {'name': 'Best Cultural Event of the Year', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-calendar-alt', 'description': 'Recognizing the best cultural event.'},
    {'name': 'Best African Art Ambassador', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-globe-africa', 'description': 'Honoring ambassadors of African art.'},
    {'name': 'Best Illustration/Comic Artist', 'group': 'Visual Arts & Culture', 'icon': 'fas fa-pen-fancy', 'description': 'Awarded to the best illustrator or comic artist.'},
    
    # ============================================================
    # MEDIA & JOURNALISM
    # ============================================================
    {'name': 'Journalist of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-newspaper', 'description': 'Awarded to the best journalist.'},
    {'name': 'Best Media Personality of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-user-circle', 'description': 'Celebrating the best media personality.'},
    {'name': 'Content Creator of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-video', 'description': 'Recognizing the best content creator.'},
    {'name': 'Best News Anchor/Reporter of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-microphone', 'description': 'Honoring the best news anchor or reporter.'},
    {'name': 'Best Radio Personality of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-radio', 'description': 'Awarded to the best radio personality.'},
    {'name': 'Best Podcast of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-podcast', 'description': 'Celebrating the best podcast.'},
    {'name': 'Best Investigative Journalist of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-search', 'description': 'Recognizing excellence in investigative journalism.'},
    {'name': 'Best Media House/Broadcaster of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-building', 'description': 'Awarded to the best media house or broadcaster.'},
    {'name': 'Best Digital News Platform of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-globe', 'description': 'Celebrating the best digital news platform.'},
    {'name': 'Best Talk Show Host of the Year', 'group': 'Media & Journalism', 'icon': 'fas fa-chair', 'description': 'Honoring the best talk show host.'},
    
    # ============================================================
    # BUSINESS & ENTERPRISE
    # ============================================================
    {'name': 'Entrepreneur of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-chart-line', 'description': 'Awarded to the best entrepreneur.'},
    {'name': 'Best Business Leader of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-user-tie', 'description': 'Celebrating outstanding business leadership.'},
    {'name': 'Fastest Growing Business of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-rocket', 'description': 'Recognizing the fastest growing business.'},
    {'name': 'Most Innovative Startup of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-lightbulb', 'description': 'Honoring the most innovative startup.'},
    {'name': 'Best Small Business of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-store', 'description': 'Awarded to the best small business.'},
    {'name': 'Best Women-Led Business of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-female', 'description': 'Celebrating excellence in women-led businesses.'},
    {'name': 'Best Social Enterprise of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-hands-helping', 'description': 'Recognizing the best social enterprise.'},
    {'name': 'Best Corporate Social Responsibility Initiative', 'group': 'Business & Enterprise', 'icon': 'fas fa-heart', 'description': 'Honoring outstanding CSR initiatives.'},
    {'name': 'Best Young Entrepreneur of the Year (Under 30)', 'group': 'Business & Enterprise', 'icon': 'fas fa-trophy', 'description': 'Recognizing young entrepreneurial talent.'},
    {'name': 'Best Business Innovation of the Year', 'group': 'Business & Enterprise', 'icon': 'fas fa-microchip', 'description': 'Celebrating business innovation.'},
    
    # ============================================================
    # FINANCE & BANKING
    # ============================================================
    {'name': 'Economist of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-chart-pie', 'description': 'Awarded to the best economist.'},
    {'name': 'Financial Advisor of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-hand-holding-usd', 'description': 'Celebrating the best financial advisor.'},
    {'name': 'Best Financial Institution of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-university', 'description': 'Honoring the best financial institution.'},
    {'name': 'Best Bank of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-building', 'description': 'Awarded to the best bank.'},
    {'name': 'Best FinTech Innovation of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-mobile-alt', 'description': 'Recognizing outstanding FinTech innovation.'},
    {'name': 'Best Mobile Money Service of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-phone', 'description': 'Celebrating the best mobile money service.'},
    {'name': 'Best Financial Inclusion Initiative', 'group': 'Finance & Banking', 'icon': 'fas fa-users', 'description': 'Honoring financial inclusion excellence.'},
    {'name': 'Best Wealth Manager of the Year', 'group': 'Finance & Banking', 'icon': 'fas fa-coins', 'description': 'Awarded to the best wealth manager.'},
    {'name': 'Best Agricultural Finance Initiative', 'group': 'Finance & Banking', 'icon': 'fas fa-tractor', 'description': 'Recognizing agricultural finance excellence.'},
    {'name': 'Best Financial Literacy Advocate', 'group': 'Finance & Banking', 'icon': 'fas fa-graduation-cap', 'description': 'Celebrating financial literacy advocacy.'},
    
    # ============================================================
    # ACCOUNTING & AUDIT
    # ============================================================
    {'name': 'Accountant of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-calculator', 'description': 'Awarded to the best accountant.'},
    {'name': 'Audit Professional of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-search-plus', 'description': 'Celebrating the best audit professional.'},
    {'name': 'Best Accounting Firm of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-building', 'description': 'Honoring the best accounting firm.'},
    {'name': 'Best Tax Consultant of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-file-invoice-dollar', 'description': 'Awarded to the best tax consultant.'},
    {'name': 'Best Forensic Accountant of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-search', 'description': 'Recognizing forensic accounting excellence.'},
    {'name': 'Best Internal Auditor of the Year', 'group': 'Accounting & Audit', 'icon': 'fas fa-clipboard-check', 'description': 'Celebrating internal audit excellence.'},
    {'name': 'Best Risk Management Professional', 'group': 'Accounting & Audit', 'icon': 'fas fa-shield-alt', 'description': 'Honoring risk management professionals.'},
    
    # ============================================================
    # ENTREPRENEURSHIP
    # ============================================================
    {'name': 'Young Entrepreneur of the Year (Under 30)', 'group': 'Entrepreneurship', 'icon': 'fas fa-trophy', 'description': 'Awarded to the best young entrepreneur.'},
    {'name': 'Women in Business Award', 'group': 'Entrepreneurship', 'icon': 'fas fa-female', 'description': 'Celebrating women in business excellence.'},
    {'name': 'Social Entrepreneur of the Year', 'group': 'Entrepreneurship', 'icon': 'fas fa-hands-helping', 'description': 'Recognizing social entrepreneurship.'},
    {'name': 'Best Startup Founder of the Year', 'group': 'Entrepreneurship', 'icon': 'fas fa-rocket', 'description': 'Honoring the best startup founder.'},
    {'name': 'Most Resilient Entrepreneur of the Year', 'group': 'Entrepreneurship', 'icon': 'fas fa-shield-virus', 'description': 'Celebrating entrepreneurial resilience.'},
    {'name': 'Best Digital Entrepreneur of the Year', 'group': 'Entrepreneurship', 'icon': 'fas fa-laptop', 'description': 'Recognizing digital entrepreneurship.'},
    {'name': 'Best Women\'s Empowerment Initiative', 'group': 'Entrepreneurship', 'icon': 'fas fa-female', 'description': 'Honoring women\'s empowerment initiatives.'},
    {'name': 'Best Youth Empowerment Initiative', 'group': 'Entrepreneurship', 'icon': 'fas fa-users', 'description': 'Celebrating youth empowerment programs.'},
    
    # ============================================================
    # REAL ESTATE & CONSTRUCTION
    # ============================================================
    {'name': 'Real Estate Developer of the Year', 'group': 'Real Estate & Construction', 'icon': 'fas fa-building', 'description': 'Awarded to the best real estate developer.'},
    {'name': 'Best Construction Company of the Year', 'group': 'Real Estate & Construction', 'icon': 'fas fa-hard-hat', 'description': 'Honoring the best construction company.'},
    {'name': 'Best Real Estate Agent of the Year', 'group': 'Real Estate & Construction', 'icon': 'fas fa-handshake', 'description': 'Celebrating the best real estate agent.'},
    {'name': 'Best Affordable Housing Initiative', 'group': 'Real Estate & Construction', 'icon': 'fas fa-home', 'description': 'Recognizing affordable housing excellence.'},
    {'name': 'Best Green/Sustainable Building', 'group': 'Real Estate & Construction', 'icon': 'fas fa-leaf', 'description': 'Awarded for sustainable building projects.'},
    {'name': 'Best Interior Designer of the Year', 'group': 'Real Estate & Construction', 'icon': 'fas fa-paint-brush', 'description': 'Honoring the best interior designer.'},
    {'name': 'Best Architectural Design of the Year', 'group': 'Real Estate & Construction', 'icon': 'fas fa-drafting-compass', 'description': 'Celebrating architectural design excellence.'},
    {'name': 'Best Real Estate Technology/PropTech', 'group': 'Real Estate & Construction', 'icon': 'fas fa-microchip', 'description': 'Recognizing PropTech innovation.'},
    
    # ============================================================
    # AGRICULTURE & FOOD SECURITY
    # ============================================================
    {'name': 'Agricultural Innovator of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-lightbulb', 'description': 'Awarded to agricultural innovators.'},
    {'name': 'Farmer of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-tractor', 'description': 'Celebrating the best farmer.'},
    {'name': 'Food Security Champion of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-utensils', 'description': 'Honoring food security champions.'},
    {'name': 'Best Agribusiness of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-store', 'description': 'Recognizing the best agribusiness.'},
    {'name': 'Best Agricultural Technology/AgriTech', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-microchip', 'description': 'Awarded for agricultural technology innovation.'},
    {'name': 'Best Sustainable Farming Initiative', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-leaf', 'description': 'Celebrating sustainable farming practices.'},
    {'name': 'Best Youth Farmer of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-user-graduate', 'description': 'Recognizing young farmers.'},
    {'name': 'Best Women Farmer of the Year', 'group': 'Agriculture & Food Security', 'icon': 'fas fa-female', 'description': 'Honoring women in agriculture.'},
    
    # ============================================================
    # TRANSPORT & LOGISTICS
    # ============================================================
    {'name': 'Logistics Company of the Year', 'group': 'Transport & Logistics', 'icon': 'fas fa-truck', 'description': 'Awarded to the best logistics company.'},
    {'name': 'Transport Innovator of the Year', 'group': 'Transport & Logistics', 'icon': 'fas fa-lightbulb', 'description': 'Celebrating transport innovation.'},
    {'name': 'Best Transportation Service of the Year', 'group': 'Transport & Logistics', 'icon': 'fas fa-bus', 'description': 'Honoring the best transportation service.'},
    {'name': 'Best Logistics Technology/Innovation', 'group': 'Transport & Logistics', 'icon': 'fas fa-microchip', 'description': 'Recognizing logistics technology.'},
    {'name': 'Best Supply Chain Management of the Year', 'group': 'Transport & Logistics', 'icon': 'fas fa-link', 'description': 'Awarded for supply chain excellence.'},
    {'name': 'Best Last-Mile Delivery Service', 'group': 'Transport & Logistics', 'icon': 'fas fa-shipping-fast', 'description': 'Celebrating last-mile delivery services.'},
    {'name': 'Best Logistics Sustainability Initiative', 'group': 'Transport & Logistics', 'icon': 'fas fa-leaf', 'description': 'Recognizing sustainable logistics.'},
    
    # ============================================================
    # TOURISM & HOSPITALITY
    # ============================================================
    {'name': 'Tourism Excellence Award', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-umbrella-beach', 'description': 'Awarded for tourism excellence.'},
    {'name': 'Hospitality Professional of the Year', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-concierge-bell', 'description': 'Honoring the best hospitality professional.'},
    {'name': 'Best Hotel/Resort of the Year', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-hotel', 'description': 'Celebrating the best hotel or resort.'},
    {'name': 'Best Tourism Destination of the Year', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-map-marked-alt', 'description': 'Recognizing the best tourism destination.'},
    {'name': 'Best Eco-Tourism Initiative', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-leaf', 'description': 'Awarded for eco-tourism excellence.'},
    {'name': 'Best Cultural Tourism Experience', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-flag', 'description': 'Honoring cultural tourism experiences.'},
    {'name': 'Best African Tourism Ambassador', 'group': 'Tourism & Hospitality', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African tourism ambassadors.'},
    
    # ============================================================
    # TECHNOLOGY & INNOVATION
    # ============================================================
    {'name': 'Tech Innovator of the Year', 'group': 'Technology & Innovation', 'icon': 'fas fa-microchip', 'description': 'Awarded to the best tech innovator.'},
    {'name': 'Best Tech Startup of the Year', 'group': 'Technology & Innovation', 'icon': 'fas fa-rocket', 'description': 'Celebrating the best tech startup.'},
    {'name': 'Digital Transformation Award', 'group': 'Technology & Innovation', 'icon': 'fas fa-sync-alt', 'description': 'Honoring digital transformation excellence.'},
    {'name': 'Best Technology Solution of the Year', 'group': 'Technology & Innovation', 'icon': 'fas fa-cogs', 'description': 'Recognizing the best technology solution.'},
    {'name': 'Best Software Developer of the Year', 'group': 'Technology & Innovation', 'icon': 'fas fa-code', 'description': 'Awarded to the best software developer.'},
    {'name': 'Best Cybersecurity Professional', 'group': 'Technology & Innovation', 'icon': 'fas fa-shield-alt', 'description': 'Celebrating cybersecurity excellence.'},
    {'name': 'Best Data Analyst/Scientist', 'group': 'Technology & Innovation', 'icon': 'fas fa-chart-bar', 'description': 'Honoring data science excellence.'},
    {'name': 'Best Mobile App of the Year', 'group': 'Technology & Innovation', 'icon': 'fas fa-mobile-alt', 'description': 'Awarded to the best mobile app.'},
    {'name': 'Best Tech for Good Initiative', 'group': 'Technology & Innovation', 'icon': 'fas fa-heart', 'description': 'Recognizing tech for social good.'},
    {'name': 'Best African Tech Leader', 'group': 'Technology & Innovation', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African tech leadership.'},
    
    # ============================================================
    # DIGITAL & SOCIAL MEDIA
    # ============================================================
    {'name': 'Social Media Influencer of the Year', 'group': 'Digital & Social Media', 'icon': 'fas fa-share-alt', 'description': 'Awarded to the best social media influencer.'},
    {'name': 'Best Digital Content Creator of the Year', 'group': 'Digital & Social Media', 'icon': 'fas fa-video', 'description': 'Celebrating digital content creation.'},
    {'name': 'Best Digital Campaign of the Year', 'group': 'Digital & Social Media', 'icon': 'fas fa-ad', 'description': 'Recognizing the best digital campaign.'},
    {'name': 'Best TikTok Creator of the Year', 'group': 'Digital & Social Media', 'icon': 'fab fa-tiktok', 'description': 'Honoring the best TikTok creator.'},
    {'name': 'Best Instagram Creator of the Year', 'group': 'Digital & Social Media', 'icon': 'fab fa-instagram', 'description': 'Awarded to the best Instagram creator.'},
    {'name': 'Best YouTube Creator of the Year', 'group': 'Digital & Social Media', 'icon': 'fab fa-youtube', 'description': 'Celebrating YouTube content creation.'},
    {'name': 'Best Digital Marketing Professional', 'group': 'Digital & Social Media', 'icon': 'fas fa-chart-line', 'description': 'Recognizing digital marketing excellence.'},
    {'name': 'Best Social Media Community Building', 'group': 'Digital & Social Media', 'icon': 'fas fa-users', 'description': 'Honoring community building on social media.'},
    {'name': 'Best African Digital Influencer', 'group': 'Digital & Social Media', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African digital influencers.'},
    {'name': 'Best Viral Content of the Year', 'group': 'Digital & Social Media', 'icon': 'fas fa-fire', 'description': 'Awarded to the best viral content.'},
    
    # ============================================================
    # ARTIFICIAL INTELLIGENCE & TECH
    # ============================================================
    {'name': 'AI Innovator of the Year', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-robot', 'description': 'Awarded to the best AI innovator.'},
    {'name': 'Best AI Application of the Year', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-brain', 'description': 'Celebrating the best AI application.'},
    {'name': 'Best Machine Learning Innovation', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-chart-line', 'description': 'Recognizing machine learning innovation.'},
    {'name': 'Best AI for Social Good', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-heart', 'description': 'Honoring AI for social impact.'},
    {'name': 'Best AI Research/Development', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-flask', 'description': 'Awarded for AI research excellence.'},
    {'name': 'Best AI Education/Training Program', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-graduation-cap', 'description': 'Celebrating AI education programs.'},
    {'name': 'Best AI Startup of the Year', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-rocket', 'description': 'Recognizing the best AI startup.'},
    {'name': 'Best African AI Leader', 'group': 'Artificial Intelligence & Tech', 'icon': 'fas fa-globe-africa', 'description': 'Honoring African AI leadership.'},
    
    # ============================================================
    # EDUCATION & ACADEMIA
    # ============================================================
    {'name': 'Educator of the Year', 'group': 'Education & Academia', 'icon': 'fas fa-chalkboard-teacher', 'description': 'Awarded to the best educator.'},
    {'name': 'Fastest Growing School of the Year', 'group': 'Education & Academia', 'icon': 'fas fa-rocket', 'description': 'Recognizing the fastest growing school.'},
    {'name': 'Best Educational Institution of the Year', 'group': 'Education & Academia', 'icon': 'fas fa-university', 'description': 'Honoring the best educational institution.'},
    {'name': 'Best Teacher of the Year', 'group': 'Education & Academia', 'icon': 'fas fa-user-graduate', 'description': 'Celebrating the best teacher.'},
    {'name': 'Best Professor/Lecturer of the Year', 'group': 'Education & Academia', 'icon': 'fas fa-user-tie', 'description': 'Awarded to the best professor or lecturer.'},
    {'name': 'Best Digital Education Platform', 'group': 'Education & Academia', 'icon': 'fas fa-laptop', 'description': 'Recognizing digital education platforms.'},
    {'name': 'Best STEM Education Program', 'group': 'Education & Academia', 'icon': 'fas fa-flask', 'description': 'Honoring STEM education excellence.'},
    {'name': 'Best Online Learning Platform', 'group': 'Education & Academia', 'icon': 'fas fa-globe', 'description': 'Celebrating online learning platforms.'},
    {'name': 'Best African Education Leader', 'group': 'Education & Academia', 'icon': 'fas fa-globe-africa', 'description': 'Recognizing African education leadership.'},
    {'name': 'Best Education Technology Innovation', 'group': 'Education & Academia', 'icon': 'fas fa-microchip', 'description': 'Awarded for education technology innovation.'},
    
    # ============================================================
    # YOUTH & EMPOWERMENT
    # ============================================================
    {'name': 'Young Leader of the Year', 'group': 'Youth & Empowerment', 'icon': 'fas fa-user-graduate', 'description': 'Awarded to the best young leader.'},
    {'name': 'Youth Empowerment Advocate of the Year', 'group': 'Youth & Empowerment', 'icon': 'fas fa-hand-holding-heart', 'description': 'Celebrating youth empowerment advocates.'},
    {'name': 'Most Promising Young Talent of the Year', 'group': 'Youth & Empowerment', 'icon': 'fas fa-star', 'description': 'Recognizing promising young talent.'},
    {'name': 'Best Youth Initiative of the Year', 'group': 'Youth & Empowerment', 'icon': 'fas fa-rocket', 'description': 'Honoring the best youth initiative.'},
    {'name': 'Best Youth Entrepreneurship Program', 'group': 'Youth & Empowerment', 'icon': 'fas fa-chart-line', 'description': 'Awarded for youth entrepreneurship programs.'},
    {'name': 'Best Youth Mentorship Program', 'group': 'Youth & Empowerment', 'icon': 'fas fa-hands-helping', 'description': 'Celebrating youth mentorship.'},
    {'name': 'Best Youth Social Impact Initiative', 'group': 'Youth & Empowerment', 'icon': 'fas fa-heart', 'description': 'Recognizing youth social impact.'},
    {'name': 'Best African Youth Leader', 'group': 'Youth & Empowerment', 'icon': 'fas fa-globe-africa', 'description': 'Honoring African youth leadership.'},
    
    # ============================================================
    # HEALTHCARE & WELLNESS
    # ============================================================
    {'name': 'Healthcare Professional of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-user-md', 'description': 'Awarded to the best healthcare professional.'},
    {'name': 'Wellness Advocate of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-leaf', 'description': 'Celebrating wellness advocacy.'},
    {'name': 'Best Healthcare Facility of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-hospital', 'description': 'Honoring the best healthcare facility.'},
    {'name': 'Best Doctor of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-stethoscope', 'description': 'Awarded to the best doctor.'},
    {'name': 'Best Nurse of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-heartbeat', 'description': 'Celebrating nursing excellence.'},
    {'name': 'Best Healthcare Innovation of the Year', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-microchip', 'description': 'Recognizing healthcare innovation.'},
    {'name': 'Best Mental Health Initiative', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-brain', 'description': 'Honoring mental health initiatives.'},
    {'name': 'Best Community Health Program', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-users', 'description': 'Awarded for community health programs.'},
    {'name': 'Best African Healthcare Leader', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African healthcare leadership.'},
    {'name': 'Best Telemedicine Initiative', 'group': 'Healthcare & Wellness', 'icon': 'fas fa-phone', 'description': 'Recognizing telemedicine excellence.'},
    
    # ============================================================
    # COMMUNITY & HUMANITY
    # ============================================================
    {'name': 'Community Leader of the Year', 'group': 'Community & Humanity', 'icon': 'fas fa-users', 'description': 'Awarded to the best community leader.'},
    {'name': 'Humanitarian of the Year', 'group': 'Community & Humanity', 'icon': 'fas fa-hands-helping', 'description': 'Celebrating humanitarian excellence.'},
    {'name': 'Best Community Initiative of the Year', 'group': 'Community & Humanity', 'icon': 'fas fa-rocket', 'description': 'Honoring the best community initiative.'},
    {'name': 'Best Community Service Project', 'group': 'Community & Humanity', 'icon': 'fas fa-tools', 'description': 'Recognizing community service projects.'},
    {'name': 'Best Community Health Program', 'group': 'Community & Humanity', 'icon': 'fas fa-heartbeat', 'description': 'Awarded for community health programs.'},
    {'name': 'Best Community Youth Program', 'group': 'Community & Humanity', 'icon': 'fas fa-user-graduate', 'description': 'Celebrating community youth programs.'},
    {'name': 'Best African Community Leader', 'group': 'Community & Humanity', 'icon': 'fas fa-globe-africa', 'description': 'Honoring African community leadership.'},
    {'name': 'Best Community Volunteer of the Year', 'group': 'Community & Humanity', 'icon': 'fas fa-hand-holding-heart', 'description': 'Recognizing community volunteers.'},
    
    # ============================================================
    # HUMAN RIGHTS & ADVOCACY
    # ============================================================
    {'name': 'Human Rights Defender of the Year', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-shield-alt', 'description': 'Awarded to human rights defenders.'},
    {'name': 'Advocacy Champion of the Year', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-bullhorn', 'description': 'Celebrating advocacy champions.'},
    {'name': 'Best Women\'s Rights Advocacy', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-female', 'description': 'Honoring women\'s rights advocacy.'},
    {'name': 'Best Children\'s Rights Advocacy', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-child', 'description': 'Awarded for children\'s rights advocacy.'},
    {'name': 'Best Disability Rights Advocacy', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-wheelchair', 'description': 'Recognizing disability rights advocacy.'},
    {'name': 'Best Human Rights Organization', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-building', 'description': 'Celebrating human rights organizations.'},
    {'name': 'Best African Human Rights Leader', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-globe-africa', 'description': 'Honoring African human rights leaders.'},
    {'name': 'Best Legal Advocacy of the Year', 'group': 'Human Rights & Advocacy', 'icon': 'fas fa-gavel', 'description': 'Recognizing legal advocacy excellence.'},
    
    # ============================================================
    # FAITH & SPIRITUALITY
    # ============================================================
    {'name': 'Faith Leader of the Year', 'group': 'Faith & Spirituality', 'icon': 'fas fa-church', 'description': 'Awarded to the best faith leader.'},
    {'name': 'Spiritual Impact Award of the Year', 'group': 'Faith & Spirituality', 'icon': 'fas fa-hands-praying', 'description': 'Celebrating spiritual impact.'},
    {'name': 'Best Church/Ministry of the Year', 'group': 'Faith & Spirituality', 'icon': 'fas fa-building', 'description': 'Honoring the best church or ministry.'},
    {'name': 'Best Bible Teacher/Preacher of the Year', 'group': 'Faith & Spirituality', 'icon': 'fas fa-bible', 'description': 'Awarded to the best Bible teacher or preacher.'},
    {'name': 'Best Youth Ministry of the Year', 'group': 'Faith & Spirituality', 'icon': 'fas fa-user-graduate', 'description': 'Celebrating youth ministry excellence.'},
    {'name': 'Best Community Outreach Ministry', 'group': 'Faith & Spirituality', 'icon': 'fas fa-hands-helping', 'description': 'Recognizing community outreach ministries.'},
    {'name': 'Best Faith-Based Organization', 'group': 'Faith & Spirituality', 'icon': 'fas fa-handshake', 'description': 'Honoring faith-based organizations.'},
    {'name': 'Best Interfaith Initiative', 'group': 'Faith & Spirituality', 'icon': 'fas fa-hand-holding-heart', 'description': 'Awarded for interfaith initiatives.'},
    {'name': 'Best African Faith Leader', 'group': 'Faith & Spirituality', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African faith leadership.'},
    {'name': 'Most Impactful Faith-Based Online Community', 'group': 'Faith & Spirituality', 'icon': 'fas fa-globe', 'description': 'Recognizing the most impactful faith-based online community.'},
    {'name': 'Best Faith Media/Content Creator', 'group': 'Faith & Spirituality', 'icon': 'fas fa-video', 'description': 'Awarded for faith media content creation.'},
    {'name': 'Best Faith Podcast/Radio Program', 'group': 'Faith & Spirituality', 'icon': 'fas fa-podcast', 'description': 'Celebrating faith podcast and radio programs.'},
    {'name': 'Best Faith and Social Justice', 'group': 'Faith & Spirituality', 'icon': 'fas fa-balance-scale', 'description': 'Recognizing faith and social justice initiatives.'},
    
    # ============================================================
    # LEADERSHIP & PUBLIC SERVICE
    # ============================================================
    {'name': 'Public Service Excellence Award', 'group': 'Leadership & Public Service', 'icon': 'fas fa-handshake', 'description': 'Awarded for public service excellence.'},
    {'name': 'Leadership Impact Award of the Year', 'group': 'Leadership & Public Service', 'icon': 'fas fa-trophy', 'description': 'Celebrating leadership impact.'},
    {'name': 'Best Public Administrator of the Year', 'group': 'Leadership & Public Service', 'icon': 'fas fa-user-tie', 'description': 'Honoring public administration excellence.'},
    {'name': 'Best Public Policy Leader of the Year', 'group': 'Leadership & Public Service', 'icon': 'fas fa-file-alt', 'description': 'Recognizing public policy leadership.'},
    {'name': 'Best African Political Leader', 'group': 'Leadership & Public Service', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African political leadership.'},
    {'name': 'Best Local Government Leader', 'group': 'Leadership & Public Service', 'icon': 'fas fa-city', 'description': 'Awarded to local government leaders.'},
    {'name': 'Best Crisis Management Leadership', 'group': 'Leadership & Public Service', 'icon': 'fas fa-shield-virus', 'description': 'Recognizing crisis management leadership.'},
    {'name': 'Best Public Service Integrity Award', 'group': 'Leadership & Public Service', 'icon': 'fas fa-shield-alt', 'description': 'Honoring public service integrity.'},
    {'name': 'Best Community Development Officer', 'group': 'Leadership & Public Service', 'icon': 'fas fa-users', 'description': 'Celebrating community development officers.'},
    
    # ============================================================
    # SPORTS & ATHLETICS
    # ============================================================
    {'name': 'Sports Personality of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-trophy', 'description': 'Awarded to the best sports personality.'},
    {'name': 'Best Athlete of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-running', 'description': 'Celebrating the best athlete.'},
    {'name': 'Rising Star in Sports of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-star', 'description': 'Recognizing rising sports stars.'},
    {'name': 'Sports Team of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-users', 'description': 'Honoring the best sports team.'},
    {'name': 'Best Footballer of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-futbol', 'description': 'Awarded to the best footballer.'},
    {'name': 'Best Basketball Player of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-basketball-ball', 'description': 'Celebrating basketball excellence.'},
    {'name': 'Best Sports Coach of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-chalkboard-teacher', 'description': 'Recognizing coaching excellence.'},
    {'name': 'Best Sports Administrator of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-tasks', 'description': 'Honoring sports administration.'},
    {'name': 'Best Esports Gamer of the Year', 'group': 'Sports & Athletics', 'icon': 'fas fa-gamepad', 'description': 'Awarded to the best esports gamer.'},
    {'name': 'Best African Sports Ambassador', 'group': 'Sports & Athletics', 'icon': 'fas fa-globe-africa', 'description': 'Celebrating African sports ambassadors.'},
    
    # ============================================================
    # ENVIRONMENT & SUSTAINABILITY
    # ============================================================
    {'name': 'Environmental Champion of the Year', 'group': 'Environment & Sustainability', 'icon': 'fas fa-leaf', 'description': 'Awarded to environmental champions.'},
    {'name': 'Sustainability Leader of the Year', 'group': 'Environment & Sustainability', 'icon': 'fas fa-recycle', 'description': 'Celebrating sustainability leadership.'},
    {'name': 'Green Innovation Award of the Year', 'group': 'Environment & Sustainability', 'icon': 'fas fa-lightbulb', 'description': 'Recognizing green innovation.'},
    {'name': 'Best Climate Action Initiative', 'group': 'Environment & Sustainability', 'icon': 'fas fa-cloud-sun', 'description': 'Honoring climate action initiatives.'},
    {'name': 'Best Conservation Project of the Year', 'group': 'Environment & Sustainability', 'icon': 'fas fa-tree', 'description': 'Awarded for conservation projects.'},
    {'name': 'Best Clean Energy Project', 'group': 'Environment & Sustainability', 'icon': 'fas fa-solar-panel', 'description': 'Celebrating clean energy projects.'},
    {'name': 'Best Environmental Education Program', 'group': 'Environment & Sustainability', 'icon': 'fas fa-graduation-cap', 'description': 'Recognizing environmental education.'},
    {'name': 'Best African Environmental Leader', 'group': 'Environment & Sustainability', 'icon': 'fas fa-globe-africa', 'description': 'Honoring African environmental leaders.'},
    {'name': 'Best Green Business of the Year', 'group': 'Environment & Sustainability', 'icon': 'fas fa-building', 'description': 'Awarded to green businesses.'},
    {'name': 'Best Environmental NGO/Organization', 'group': 'Environment & Sustainability', 'icon': 'fas fa-handshake', 'description': 'Celebrating environmental organizations.'},
    {'name': 'Best Environmental Technology', 'group': 'Environment & Sustainability', 'icon': 'fas fa-microchip', 'description': 'Recognizing environmental technology.'},
]

class Command(BaseCommand):
    help = 'Seeds the database with all award categories'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding categories...')
        
        created_count = 0
        skipped_count = 0
        updated_count = 0
        
        for cat_data in AWARD_CATEGORIES:
            # Check if category already exists by name and group
            existing = Category.objects.filter(
                name=cat_data['name'],
                group=cat_data['group']
            ).first()
            
            if existing:
                # Check if any fields need updating
                needs_update = False
                if existing.icon != cat_data.get('icon', 'fas fa-award'):
                    existing.icon = cat_data.get('icon', 'fas fa-award')
                    needs_update = True
                if existing.description != cat_data.get('description', ''):
                    existing.description = cat_data.get('description', '')
                    needs_update = True
                
                if needs_update:
                    existing.save()
                    updated_count += 1
                    self.stdout.write(f'  ↻ Updated: {cat_data["name"]}')
                else:
                    skipped_count += 1
                continue
            
            # Create new category
            try:
                Category.objects.create(
                    name=cat_data['name'],
                    group=cat_data['group'],
                    description=cat_data.get('description', ''),
                    icon=cat_data.get('icon', 'fas fa-award'),
                    is_active=True
                )
                created_count += 1
                self.stdout.write(f'  ✓ Created: {cat_data["name"]}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating {cat_data["name"]}: {str(e)}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'✅ Done! Created {created_count} categories, updated {updated_count}, skipped {skipped_count} existing.'
        ))
        self.stdout.write(f'📊 Total categories in database: {Category.objects.count()}')