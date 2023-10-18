import { IMovieAdvancedCard } from 'src/types/MovieByAdvancedSearch.types';
import { API_BASE_URL } from 'src/utils/constants';
import { IData } from 'src/types/MovieByAdvancedSearch.types';

const checkRes = (res: Response) => {
	if (res.ok) {
		return res.json();
	} else {
		return Promise.reject(res);
	}
};

export const fetchData = (url: string, method: string, token?: string) => {
	return fetch(url, {
		method,
		headers: {
			'Content-Type': 'application/json',
			...(!!token && { Authorization: `Token ${token}` }),
		},
	}).then((res) => checkRes(res));
};

export const getMovieByAdvancedSearch = (
	data: IData,
	token: string
): Promise<IMovieAdvancedCard[]> => {
	return fetchData(
		`${API_BASE_URL}/movies/?actor=${data.actor}&director=${data.director}&genre=${data.genre}&country=${data.country}&year_gt=${data.yearFrom}&year_lt=${data.yearTo}&imdb_rate_gt=${data.ratingFrom}&imdb_rate_lt=${data.ratingTo}`,
		'GET',
		token
	);
};

export const getMovieBySearch = (
	values: any,
	token: string
): Promise<IMovieAdvancedCard[]> => {
	return fetchData(`${API_BASE_URL}/movies/?title=${values}`, 'GET', token);
};
