import random
import numpy as np
import pandas as pd
from database import LoadData
from userclass import User

__version__ = 0.0001


class Quiz(object):
    def __init__(self, categories_num: int = 5):
        self.user_data = User
        self.ld = LoadData()
        self.questions_num = 4
        self.categories_num: int = categories_num
        self.unq_categories = np.arange(self.categories_num)
        self.all_categories_questions: list = []
        self.q_a_matrix_rows = categories_num
        self.q_a_matrix_cols = self.questions_num
        self.all_categories_questions_idxs = np.zeros([self.q_a_matrix_rows, self.q_a_matrix_cols])
        self.user_all_q_a: dict = {}
        self.current_answers_random_order = []
        self.answers_num = 5
        self.default_answers_order = range(self.answers_num)
        self.current_answers_cols_order: list = []
        self.answers_cos_dict = {0: 'correct',
                                 1: 'not_correct_1',
                                 2: 'not_correct_2',
                                 3: 'not_correct_3',
                                 4: 'not_correct_4',
                                 }
        self.all_categories_questions_used = np.empty([self.q_a_matrix_rows, self.q_a_matrix_cols], dtype=bool)
        self.user_route: dict = {}
        self.questions_count = 0
        self.user_score = 0
        self.question_row_idx = 0
        self.question_col_idx = 0
        self.end_game_flag = False
        self.choose_categories()
        self.prepare_questions()
        self.status = 0 #0 - name, 1 - table, 2 - answer,
        pass

    def get_one_cat_questions(self, cat_num):
        questions = self.ld.get_lines_by_category(cat_num)
        questions_out = questions.sample(n=4, random_state=42)
        questions_out = questions_out.sort_values('score')
        return questions_out

    def choose_categories(self) -> None:
        """ take list of question categories from DB.
        Leave just unique and calculate count questions each category.
        If count of questions in category is 4 or more keep for use
        Take from category list just self.categories_num elements in random sequence.

        return:
            list of unique categories"""
        categories = self.ld.get_column('cat_num').tolist()
        unq_categories, unq_counts = np.unique(categories, return_counts=True)
        unq_categories = unq_categories[unq_counts >= self.q_a_matrix_cols]
        unq_categories = list(unq_categories)
        # TODO: add check and get only ONE question from each unique score_group
        self.unq_categories = random.sample(unq_categories, k=self.categories_num)
        pass

    def prepare_questions(self):
        all_categories_questions_idxs: list = []
        for cat_num in self.unq_categories:

            cat_questions = self.get_one_cat_questions(cat_num)
            cat_questions_idxs = cat_questions.index.tolist()
            self.all_categories_questions.append(cat_questions)
            all_categories_questions_idxs.append(cat_questions_idxs)
        self.all_categories_questions_idxs = np.asarray(all_categories_questions_idxs)
        pass

    def create_rows_cols_pic_box(self):
        """
        Returns:
            pic_matrix (list):      list of lists with str for buttons and picture creating
            array_idxs (np.array):  array with question indxs
        """
        pic_matrix: list = []
        for row_idx in range(self.q_a_matrix_rows):
            row_list: list = []
            q_a = self.get_q_a(row_idx, 0)
            row_list.append(q_a['category'].item())
            if not self.all_categories_questions_used[row_idx, 0]:
                row_list.append(str(q_a['score'].item()))
            else:
                row_list.append('-')

            for cols_idx in range(1, self.q_a_matrix_cols):
                if not self.all_categories_questions_used[row_idx, cols_idx]:
                    q_a = self.get_q_a(row_idx, cols_idx)
                    row_list.append(str(q_a['score'].item()))
                else:
                    row_list.append('-')
            pic_matrix.append(row_list)
        return pic_matrix

    def get_q_a(self, row_idx, col_idx) -> pd.DataFrame:
        question_idx = self.all_categories_questions_idxs[row_idx, col_idx]
        q_a = self.ld.db[self.ld.db.index == question_idx]
        return q_a

    def get_question_and_answers(self, row_idx: int, col_idx: int):
        self.questions_count += 1
        self.current_answers_cols_order = list()
        self.question_row_idx = row_idx
        self.question_col_idx = col_idx
        q_a = self.get_q_a(self.question_row_idx, self.question_col_idx)
        self.current_answers_random_order = random.sample(self.default_answers_order, self.answers_num)
        answers_list: list = []
        for answer_num in self.current_answers_random_order:
            col_name = self.answers_cos_dict[answer_num]
            answer = q_a[col_name].item()
            answers_list.append([answer])
            self.current_answers_cols_order.append(col_name)
            pass
        """ True => question used """
        self.all_categories_questions_used[self.question_row_idx, self.question_col_idx] = True
        question = q_a.question.item()
        return question, answers_list

    def check_answer(self, answer_num):
        is_answer_correct = False
        q_a = self.get_q_a(self.question_row_idx, self.question_col_idx)
        if self.current_answers_random_order[answer_num] == 0:
            is_answer_correct = True
        user_answer_col = self.current_answers_cols_order[answer_num]
        user_answer_msg = q_a[user_answer_col].item()
        correct_answer_msg = q_a['correct'].item()
        if is_answer_correct:
            self.user_score += int(q_a.score.item())
            self.user_data.score = self.user_score
        user_true_answer_num = self.current_answers_random_order[answer_num]
        user_answer_data: dict = {}
        answer_data = list()
        answer_data.append(is_answer_correct)
        answer_data.append(user_true_answer_num)
        user_answer_data.update({int(q_a.index.item()): answer_data})
        self.user_route.update({self.questions_count: user_answer_data})
        # print(self.user_route)
        have_questions = np.count_nonzero(self.all_categories_questions_used)
        if have_questions == self.q_a_matrix_rows*self.q_a_matrix_cols:
            self.end_game_flag = True
        full_answer = q_a['comment'].item()
        return is_answer_correct, user_answer_msg, correct_answer_msg, full_answer

    def get_user_stats(self):
        return self.user_route, self.user_score


if __name__ == "__main__":
    q = Quiz()
    print(q.all_categories_questions)
    print(q.get_q_a(2, 3))
    pic_list, _ = q.create_rows_cols_pic_box()
    # pic = q.get_board_pic(pic_list)
    # print(q.get_question_and_answers(2, 3))
    print(pic_list)

