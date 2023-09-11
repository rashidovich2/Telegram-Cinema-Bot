from kinopoisk import movie
from src import config


class Parser:
    def __init__(self):
        self.output = ""
        self.full_output = ""
        self.photo = None
        self.name = ""
        self.id = 1

    def parse_text(self, text):
        Parser.__init__(self)
        m = movie.Movie()
        movie_list = m.objects.search(text)
        if len(movie_list) == 0:
            return config.err_msg(text)
        output_text = f'По запросу \"{text}\" найдено:\n'
        for item in movie_list[:8]:
            title = item.title
            year = item.year
            rating = item.rating
            id = item.id
            if item.series:
                title = title + " (сериал)\t"
            if item.title_en:
                title = f"{title} ({item.title_en})"
            if rating is None:
                rating = "Нет данных"
            output_text += f"● {title}\n📅: {year}\t⭐️ {rating}\t/i{id} ️\n"
        return output_text

    # "● Криминальное чтиво [1995; /i342]"

    def parse_id(self, film_id):
        mov = movie.Movie(id=film_id)
        mov.get_content("main_page")
        mov.get_content("posters")
        mov.get_content("trailers")
        # Title
        title = f"{mov.title}"
        self.name = title
        self.id = film_id
        if mov.series:
            title += " (сериал)"
        self.full_output = title + '\n'
        year = mov.year
        genre = mov.genres[0]
        countries = mov.countries[0]
        self.output = f"{title},\t [{year}, {genre}, {countries}] \n"
        if mov.title_en:
            self.output += f"\t({mov.title_en})\n"
            self.full_output += f"\t({mov.title_en})\n"
        # Tagline
        if len(mov.tagline) > 0:
            self.full_output += f"📢 {mov.tagline}\n"
        # Rating
        if mov.rating is not None:
            self.output += f"⭐️ {mov.rating}\n"
            self.full_output += f"⭐️ {mov.rating}\n"
        # Date
        if mov.year is not None:
            self.full_output += f"📅️ {mov.year}\n"
        # Duration
        if mov.runtime is not None:
            self.output += f"⏱️ {mov.runtime} мин.\n"
            self.full_output += f"⏱️ {mov.runtime} мин.\n"
        # Genres
        if len(mov.genres) > 0:
            genres = ", ".join(mov.genres)
            self.full_output += f"🎭 {genres}\n"
        # Countries
        if len(mov.countries) > 0:
            countries = ", ".join(mov.countries)
            self.full_output += f"🌍 {countries}\n"
        # Actors
        if len(mov.actors):
            actors = ', '.join(map(lambda x: x.name, mov.actors))
            self.full_output += f"👥 {actors}\n"
            actors = ', '.join(map(lambda x: x.name, mov.actors[:3]))
            self.output += f"👥 {actors}, ...\n"
        # Directors
        if len(mov.directors) > 0:
            directors = ", ".join(map(lambda x: x.name, mov.directors))
            self.full_output += f"🎬 {directors}\n"
        # Composers
        if len(mov.composers) > 0:
            composers = ", ".join(map(lambda x: x.name, mov.composers))
            self.full_output += f"🎵 {composers}\n"
        if len(mov.trailers) > 0:
            trailer = mov.trailers[0].file
            self.output += f'🎥 Посмотреть [трейлер]({f"https://www.kinopoisk.ru/{trailer}"}).\n'
            self.full_output += f'🎥 Посмотреть [трейлер]({f"https://www.kinopoisk.ru/{trailer}"}).\n'
        # Plot
        if len(mov.plot) > 0:
            plot = ". ".join(mov.plot.split('.'))
            self.full_output += f"📖 {plot}\n"
            plot = ". ".join(mov.plot.split('.')[:2])
            self.output += f"📖 {plot} ...\n"
        if len(mov.url) > 0:
            self.output += f"Страница на [Кинопоиске]({mov.url})"
            self.full_output += f"Страница на [Кинопоиске]({mov.url})"
        # Poster
        if len(mov.posters) > 0:
            self.photo = mov.posters[0]


