import { Link } from 'react-router-dom';
import { BaseSyntheticEvent, useEffect, useState } from 'react';
import './ProfilePage.css';
import Input from 'src/components/Input/Input';
import { InputColors, InputTypes } from 'src/types/Input.types';
import { useAppDispatch, useAppSelector } from 'src/services/typeHooks';
import {
	editUserInfo,
	getUserInfo,
	selectUser,
	selectUserStatus,
} from 'src/services/redux/slices/user/user';
import Button from 'src/components/Button/Button';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import { IEditProfileFields } from 'src/types/Auth.types';
import { selectGenres } from 'src/services/redux/slices/genres/genres';
import GenreCheckbox from 'src/components/GenreCheckbox/GenreCheckbox';

import { format } from 'date-fns';
import DeleteProfilePopup from 'src/components/Popup/DeleteProfilePopup';
import ChangesSavedPopup from 'src/components/Popup/ChangesSavedPopup';
import ChangeAvatarPopup from 'src/components/Popup/ChangeAvatarPopup';
import { Loader } from 'src/components/Loader/Loader';
import arrow from '../../images/Chevron.svg';
import comedy from 'src/images/avatar/comedy.svg';
import { getAvatarsApi } from 'src/services/redux/slices/avatars/avatars';

const ProfilePage = () => {
	const dispatch = useAppDispatch();
	const user = useAppSelector(selectUser);
	const status = useAppSelector(selectUserStatus);
	const genres = useAppSelector(selectGenres);
	// const savedImage = useAppSelector((state) => state.avatars.savedImage);

	const [isDeletePopupOpened, setIsDeletePopupOpened] =
		useState<boolean>(false);
	const [isSavedPopupOpened, setIsSavedPopupOpened] = useState<boolean>(false);
	const [isAvatarPopupOpened, setIsAvatarPopupOpened] =
		useState<boolean>(false);

	const {
		handleSubmit,
		control,
		getValues,
		setValue,
		register,
		watch,
		reset,
		formState: { errors, isDirty, isValid, dirtyFields },
	} = useForm<IEditProfileFields>({
		mode: 'onChange',
	});

	const avatars = useAppSelector((state) => state.avatars.images);

	const avatarObject = avatars.find((avatar) => avatar.id === user.avatar);
	const avatarUrl = avatarObject ? avatarObject.avatar : '';

	const onSubmit: SubmitHandler<IEditProfileFields> = (
		values: IEditProfileFields
	) => {
		dispatch(
			editUserInfo({
				data: {
					username: getValues('nickname'),
					date_of_birth: getValues('dateOfBirth')
						? getValues('dateOfBirth')
						: user.dateOfBirth,
					sex: getValues('sex') || null,
				},
				token: user.token,
			})
		)
			.unwrap()
			.then(() => {
				setIsSavedPopupOpened(true);
				reset(values);
			})
			.catch((err: unknown) => console.log('editUserInfo err', err));
	};

	const validateDate = (value: string) => {
		if (value === undefined) return true;
		else {
			const parsedDate = format(new Date(value), 'yyyy-MM-dd');

			if (parsedDate !== value) {
				return 'Некорректный формат даты (дд-мм-гггг)';
			}

			return true;
		}
	};

	useEffect(() => {
		if (user.token) {
			dispatch(getUserInfo(user.token))
				.unwrap()
				.then(() => {
					if (user.nickname) {
						setValue('nickname', user.nickname);
					}
					if (user.dateOfBirth) {
						setValue('dateOfBirth', user.dateOfBirth);
					}
				})
				.catch((err: unknown) => console.log('getUserInfo err', err));
		}
	}, [dispatch]);

	useEffect(() => {
		if (user.token) {
			dispatch(getAvatarsApi(user.token));
		}
	}, []);

	return status === 'loading' ? (
		<Loader />
	) : (
		<>
			<main className="profile" id="profile-page">
				<div className="profile__container profile__container_type_desktop">
					<div className="profile__form-container">
						<h1 className="profile__title">Профиль</h1>
						<form className="profile__form" onSubmit={handleSubmit(onSubmit)}>
							<Input
								inputType={InputTypes.email}
								color={InputColors.black}
								labelText="Электронная почта"
								readOnly
								value={user.email}
							/>
							<div className="profile__pseudo-input-container">
								<Input
									inputType={InputTypes.password}
									color={InputColors.black}
									labelText="Пароль"
									readOnly
									value=".........."
								/>
								<Link to={'/reset-password'} className="profile__input-link">
									Изменить пароль
								</Link>
							</div>
							<Controller
								name="nickname"
								control={control}
								rules={{
									required: false,
									pattern: {
										value: /^[A-Za-zА-Яа-яЁё]{1,32}$/,
										message: 'Только кириллица или латинские буквы',
									},
									maxLength: {
										value: 32,
										message: 'Максимум 32 символа',
									},
								}}
								render={({ field }) => (
									<Input
										inputType={InputTypes.text}
										color={InputColors.black}
										labelText="Никнейм"
										defaultValue={user.nickname}
										onChange={(e: BaseSyntheticEvent) => {
											field.onChange(e);
											setValue('nickname', e.target.value);
										}}
										error={
											errors.nickname && errors.nickname.message?.toString()
										}
									/>
								)}
							/>
							<Controller
								name="dateOfBirth"
								control={control}
								defaultValue={user.dateOfBirth ? user.dateOfBirth : undefined}
								rules={{
									required: false,
									pattern: {
										value: /^\d{4}-\d{2}-\d{2}$/,
										message: 'Некорректный формат даты',
									},
									min: {
										value: '1923-01-01',
										message: 'Неверный формат значения «Дата рождения»',
									},
									max: {
										value: '2018-01-01',
										message: 'Неверный формат значения «Дата рождения»',
									},
									validate: validateDate,
								}}
								render={({ field }) => (
									<Input
										inputType={InputTypes.date}
										color={InputColors.black}
										labelText="Дата рождения"
										defaultValue={user.dateOfBirth}
										value={
											dirtyFields.dateOfBirth
												? watch('dateOfBirth')
												: user.dateOfBirth
										}
										onChange={(e: BaseSyntheticEvent) => {
											field.onChange(e);
											setValue('dateOfBirth', e.target.value, {
												shouldDirty: true,
											});
										}}
										max={'2018-08-03'}
										error={
											errors.dateOfBirth &&
											errors.dateOfBirth.message?.toString()
										}
									/>
								)}
							/>
							<div>
								<p className="profile__radio-title">Пол</p>
								<div className="profile__radio-buttons">
									<label htmlFor="male" className="profile__radio-label">
										<input
											{...register('sex')}
											type="radio"
											className="profile__radio-button"
											id="male"
											value={0}
											onChange={() => setValue('sex', 0, { shouldDirty: true })}
											checked={
												dirtyFields.sex ? watch('sex') === 0 : user.sex === 0
											}
										/>
										<span className="profile__radio-pseudo-item"></span>
										<span className="profile__radio-text">Мужской</span>
									</label>
									<label htmlFor="female" className="profile__radio-label">
										<input
											{...register('sex')}
											type="radio"
											className="profile__radio-button"
											id="female"
											value={1}
											onChange={() => setValue('sex', 1, { shouldDirty: true })}
											checked={
												dirtyFields.sex ? watch('sex') === 1 : user.sex === 1
											}
										/>
										<span className="profile__radio-pseudo-item"></span>
										<span className="profile__radio-text">Женский</span>
									</label>
								</div>
							</div>
						</form>
					</div>
					<div className="profile__avatar-container">
						<div
							className={
								user.avatar && user.avatar !== 0
									? 'profile__avatar '
									: 'profile__avatar  profile__avatar_type_letter'
							}
						>
							<button
								type="button"
								className="profile__avatar-btn"
								onClick={() => setIsAvatarPopupOpened(true)}
							></button>
							{user.avatar && user.avatar !== 0 ? (
								<img className="profile__avatar-img" src={avatarUrl} />
							) : (
								<p className="profile__user-first-letter">
									{user.nickname ? user.nickname[0] : user.email[0]}
								</p>
							)}
						</div>
						<div className="profile__buttons">
							<Button
								buttonText={'Сохранить'}
								type="submit"
								handleButtonClick={handleSubmit(onSubmit)}
								disabled={!isDirty || !isValid}
							/>
							<Button
								className={'profile__delete-button'}
								buttonText={'Удалить профиль'}
								type={'button'}
								handleButtonClick={() => setIsDeletePopupOpened(true)}
							/>
						</div>
					</div>
				</div>
				<div className="profile__container profile__container_type_mobile">
					<div className="profile__form-container">
						<h1 className="profile__title">Профиль</h1>
						<div
							className={
								user.avatar && user.avatar !== 0
									? 'profile__avatar '
									: 'profile__avatar  profile__avatar_type_letter'
							}
						>
							<button
								type="button"
								className="profile__avatar-btn"
								onClick={() => setIsAvatarPopupOpened(true)}
							></button>
							{user.avatar && user.avatar !== 0 ? (
								<img className="profile__avatar-img" src={avatarUrl} />
							) : (
								<p className="profile__user-first-letter">
									{user.nickname ? user.nickname[0] : user.email[0]}
								</p>
							)}
						</div>
						<form className="profile__form" onSubmit={handleSubmit(onSubmit)}>
							<Input
								inputType={InputTypes.email}
								color={InputColors.black}
								labelText="Электронная почта"
								readOnly
								value={user.email}
							/>
							<div className="profile__pseudo-input-container">
								<Input
									inputType={InputTypes.password}
									color={InputColors.black}
									labelText="Пароль"
									readOnly
									value=".........."
								/>
								<Link to={'/reset-password'} className="profile__input-link">
									Изменить пароль
								</Link>
							</div>
							<Controller
								name="nickname"
								control={control}
								rules={{
									required: false,
									pattern: {
										value: /^[A-Za-zА-Яа-яЁё]{1,32}$/,
										message: 'Только кириллица или латинские буквы',
									},
									maxLength: {
										value: 32,
										message: 'Максимум 32 символа',
									},
								}}
								render={({ field }) => (
									<Input
										inputType={InputTypes.text}
										color={InputColors.black}
										labelText="Никнейм"
										defaultValue={user.nickname}
										onChange={(e: BaseSyntheticEvent) => {
											field.onChange(e);
											setValue('nickname', e.target.value);
										}}
										error={
											errors.nickname && errors.nickname.message?.toString()
										}
									/>
								)}
							/>
							<Controller
								name="dateOfBirth"
								control={control}
								defaultValue={user.dateOfBirth ? user.dateOfBirth : undefined}
								rules={{
									required: false,
									pattern: {
										value: /^\d{4}-\d{2}-\d{2}$/,
										message: 'Некорректный формат даты',
									},
									min: {
										value: '1923-01-01',
										message: 'Неверный формат значения «Дата рождения»',
									},
									max: {
										value: '2018-01-01',
										message: 'Неверный формат значения «Дата рождения»',
									},
									validate: validateDate,
								}}
								render={({ field }) => (
									<Input
										inputType={InputTypes.date}
										color={InputColors.black}
										labelText="Дата рождения"
										defaultValue={user.dateOfBirth}
										value={
											dirtyFields.dateOfBirth
												? watch('dateOfBirth')
												: user.dateOfBirth
										}
										onChange={(e: BaseSyntheticEvent) => {
											field.onChange(e);
											setValue('dateOfBirth', e.target.value, {
												shouldDirty: true,
											});
										}}
										max={'2018-08-03'}
										error={
											errors.dateOfBirth &&
											errors.dateOfBirth.message?.toString()
										}
									/>
								)}
							/>
							<div>
								<p className="profile__radio-title">Пол</p>
								<div className="profile__radio-buttons">
									<label htmlFor="male" className="profile__radio-label">
										<input
											{...register('sex')}
											type="radio"
											className="profile__radio-button"
											id="male"
											value={0}
											onChange={() => setValue('sex', 0, { shouldDirty: true })}
											checked={
												dirtyFields.sex ? watch('sex') === 0 : user.sex === 0
											}
										/>
										<span className="profile__radio-pseudo-item"></span>
										<span className="profile__radio-text">Мужской</span>
									</label>
									<label htmlFor="female" className="profile__radio-label">
										<input
											{...register('sex')}
											type="radio"
											className="profile__radio-button"
											id="female"
											value={1}
											onChange={() => setValue('sex', 1, { shouldDirty: true })}
											checked={
												dirtyFields.sex ? watch('sex') === 1 : user.sex === 1
											}
										/>
										<span className="profile__radio-pseudo-item"></span>
										<span className="profile__radio-text">Женский</span>
									</label>
								</div>
							</div>
						</form>
						<Link to="/preferences" className="profile__genres-btn">
							<h2 className="profile__genres-btn-text">Избранные жанры</h2>
							<img
								className="profile__genres-btn-img"
								alt="Стрелка"
								src={arrow}
							/>
						</Link>
					</div>
					<div className="profile__avatar-container">
						<div className="profile__buttons">
							<Button
								buttonText={'Сохранить'}
								type="submit"
								handleButtonClick={handleSubmit(onSubmit)}
								disabled={!isDirty || !isValid}
							/>
							<Button
								className={'profile__delete-button'}
								buttonText={'Удалить профиль'}
								type={'button'}
								handleButtonClick={() => setIsDeletePopupOpened(true)}
							/>
						</div>
					</div>
				</div>
				<div className="profile__genres-container">
					<h3 className="profile__genres-title">Избранные жанры</h3>
					<ul className="profile__genres">
						{user.fav_genres &&
							genres
								.filter((genre) => user.fav_genres.includes(genre.id))
								.map((genre) => (
									<li className="profile__genre" key={genre.id}>
										<GenreCheckbox
											text={genre.title}
											id={genre.id}
											color="yellow"
											checked={true}
											readOnly={true}
										/>
									</li>
								))}
					</ul>
					<Link
						className="profile__genres-link"
						style={!user.fav_genres?.length ? { margin: 0 } : undefined}
						to="/preferences"
					>
						Редактировать жанры
					</Link>
				</div>
			</main>
			<DeleteProfilePopup
				isOpened={isDeletePopupOpened}
				setIsOpened={setIsDeletePopupOpened}
			/>
			<ChangesSavedPopup
				isOpened={isSavedPopupOpened}
				setIsOpened={setIsSavedPopupOpened}
			/>
			<ChangeAvatarPopup
				isOpened={isAvatarPopupOpened}
				setIsOpened={setIsAvatarPopupOpened}
			/>
		</>
	);
};

export default ProfilePage;
