from PySide2.QtWidgets import QPushButton, QMainWindow, QLabel, QLineEdit, QGroupBox
from math import ceil
import source


class MainWindow:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_ratio = screen_width / 3840
        self.half_screen_ratio = 0.45 + self.screen_ratio / 2
        self.production_speed_ratio = 1
        self.window = QMainWindow()
        self.window.resize(self.screen_width, self.screen_height)
        self.window.setWindowTitle('戴森球计划产量计算器 ver.0.1')
        self.grid_width = 75 * self.screen_ratio
        self.grid_height = 50 * self.screen_ratio
        self.init_bias = 50 * self.screen_ratio
        self.interval = 0 * self.screen_ratio
        self.box_width = self.grid_width * 4 + self.interval + 5 * self.screen_ratio
        self.box_height = self.grid_height * 2 + self.init_bias + 5 * self.screen_ratio

        # Subtitle: app name - author
        self.subtitle_font_size = 50 * self.screen_ratio
        if self.screen_ratio > 0.7:
            self.subtitle_font_size = 50 * self.screen_ratio / 1.5
        subtitle = QLabel(self.window)
        subtitle.setText('戴森球计划 材料生产计算器 -- by 魂月')
        subtitle.setStyleSheet('QLabel {font: 75 ' + str(int(self.subtitle_font_size)) + 'pt "宋体";}')
        subtitle.move(1000 * self.screen_ratio, int(25 * self.screen_ratio))
        subtitle.resize(1840 * self.screen_ratio, self.box_height * self.screen_ratio)

        # Bottom: 取整机器数量
        self.button = QPushButton('取整机器数量', self.window)
        self.button.move(2840 * self.screen_ratio, int(25 * self.screen_ratio) + int(self.box_height / 3))
        self.button.resize(400 * self.screen_ratio, int(self.box_height / 3))
        self.button.setStyleSheet('QPushButton {font: ' + str(int(self.subtitle_font_size / 2)) + 'pt "宋体";}')
        self.button.clicked.connect(self.ceil_machine_number)

        self.ox = (self.screen_width - 12 * self.box_width) / 2
        self.oy = self.box_height + 50 * self.screen_ratio
        self.font_size = 14 * self.half_screen_ratio
        self.line_edit_font_size = self.font_size * 0.9
        if self.screen_ratio < 0.45:
            self.line_edit_font_size = self.font_size * 0.75
        self.element = source.element
        self.production = source.production
        self.supporter = source.support
        self.sorted_element = source.sorted_element
        self.element_box = [[[None, None, None, None] for _ in range(len(self.element[0]))] for _ in range(len(self.element))]
        self.element_amount = [[[0, 0, 0, 0] for _ in range(len(self.element[0]))] for _ in range(len(self.element))]
        self.map = {}
        self.table_gen()
        for k, v in self.map.items():
            for v_elem in v:
                v_elem.editingFinished.connect(self.update_table(k))

    def table_gen(self):
        nrows = len(self.element)
        ncols = len(self.element[0])
        for i in range(nrows):
            for j in range(ncols):
                foo = self.box_gen(self.ox + j * self.box_width, self.oy + i * self.box_height, self.element[i][j])
                if len(foo) == 4:
                    for k in range(4):
                        self.element_box[i][j][k] = foo[k]

    def box_gen(self, x, y, resource=''):
        group_box = QGroupBox(self.window)
        group_box.move(x, y)
        group_box.resize(self.box_width, self.box_height)
        if resource == '':
            return []
        group_box.setTitle('')
        group_box.setStyleSheet('QGroupBox { background-color: \
            rgb(255, 255, 255); border: 3px solid rgb(122, 255, 100); } \
            QGroupBox::title{font: 75 ' + str(100 * self.screen_ratio) + 'pt "宋体"; color: rgb(255, 0, 0)}')

        label_again = QLabel(group_box)
        label_again.setStyleSheet('QLabel {font: 75 ' + str(self.font_size) + 'pt "宋体"; color: rgb(255, 0, 0)}')
        label_again.setText(resource)
        label_again.move(int(self.grid_width * 0.7), 5 * self.screen_ratio)
        label_again.resize(int(self.grid_width * 3.3), self.init_bias - 5)

        product_label00 = QLabel(group_box)
        product_label00.setText('产量')
        product_label00.move(3, self.init_bias)
        product_label00.resize(self.grid_width, self.grid_height)
        product_label00.setStyleSheet('QLabel {font: 75 ' + str(self.font_size) + 'pt "宋体"}')
        product00 = QLineEdit(group_box)
        product00.setText('0')
        product00.move(self.grid_width, self.init_bias)
        product00.resize(self.grid_width, self.grid_height)
        product00.setEnabled(False)
        product00.setStyleSheet('QLineEdit {font: ' + str(self.line_edit_font_size) + 'pt "宋体"}')

        product_label10 = QLabel(group_box)
        product_label10.setText('额外')
        product_label10.move(3, self.grid_height + self.init_bias)
        product_label10.resize(self.grid_width, self.grid_height)
        product_label10.setStyleSheet('QLabel {font: 75 ' + str(self.font_size) + 'pt "宋体"}')
        product10 = QLineEdit(group_box)
        product10.setText('0')
        product10.move(self.grid_width, self.grid_height + self.init_bias)
        product10.resize(self.grid_width, self.grid_height)
        product10.setStyleSheet('QLineEdit {font: ' + str(self.line_edit_font_size) + 'pt "宋体"}')

        product_label01 = QLabel(group_box)
        product_label01.setText('机器')
        product_label01.move(self.grid_width * 2 + self.interval, self.init_bias)
        product_label01.resize(self.grid_width, self.grid_height)
        product_label01.setStyleSheet('QLabel {font: 75 ' + str(self.font_size) + 'pt "宋体"}')
        product01 = QLineEdit(group_box)
        product01.setText('0.0')
        product01.move(self.grid_width * 3 + self.interval, self.init_bias)
        product01.resize(self.grid_width, self.grid_height)
        product01.setStyleSheet('QLineEdit {font: ' + str(self.line_edit_font_size) + 'pt "宋体"}')
        product01.setEnabled(False)

        product_label11 = QLabel(group_box)
        product_label11.setText('已有')
        product_label11.move(self.grid_width * 2 + self.interval, self.grid_height + self.init_bias)
        product_label11.resize(self.grid_width, self.grid_height)
        product_label11.setStyleSheet('QLabel {font: 75 ' + str(self.font_size) + 'pt "宋体"}')
        product11 = QLineEdit(group_box)
        product11.setText('0')
        product11.move(self.grid_width * 3 + self.interval, self.grid_height + self.init_bias)
        product11.resize(self.grid_width, self.grid_height)
        product11.setStyleSheet('QLineEdit {font: ' + str(self.line_edit_font_size) + 'pt "宋体"}')
        if resource in self.supporter:
            product11.setEnabled(True)
        else:
            product11.setEnabled(False)

        self.map[resource] = [product00, product01, product10, product11]
        return [product00, product01, product10, product11]

    def get_idx(self, resource):
        idx = [-1, -1]
        if resource != '':
            for i in range(len(self.element)):
                for j in range(len(self.element[0])):
                    if resource == self.element[i][j]:
                        idx = [i, j]
        return idx

    def update_table(self, resource):
        def update_table_inner():
            # Update self.element_amount.
            for resource in self.sorted_element:
                i, j = self.get_idx(resource)
                for k in range(4):
                    input_value = self.element_box[i][j][k].text()
                    if input_value != '':
                        self.element_amount[i][j][k] = int(float(input_value))
                    else:
                        self.element_amount[i][j][k] = 0
            # Recalculate the self.element_amount.
            # 1. Set all "产量" box to be the values of their "额外" box.
            for resource in self.sorted_element:
                i, j = self.get_idx(resource)
                self.element_amount[i][j][0] = self.element_amount[i][j][2] - self.element_amount[i][j][3]
            # 2. Recalculate the values for all "产量" box.
            for produce_resource in self.sorted_element:
                i, j = self.get_idx(produce_resource)
                produce_resource_amount = self.element_amount[i][j][0]
                for component in self.production[produce_resource][1:]:
                    idx = self.get_idx(component[0])
                    self.element_amount[idx[0]][idx[1]][0] += produce_resource_amount * component[1]
            # 3. Deal with the negative values in "产量" box.
            for produce_resource in self.sorted_element:
                i, j = self.get_idx(produce_resource)
                negative_product_amount = self.element_amount[i][j][0]
                if negative_product_amount < 0:
                    if produce_resource in self.supporter:
                        for secondary_product in self.supporter[produce_resource]:
                            product_name = secondary_product[0]
                            product_amount = secondary_product[1]
                            can_be_negative = secondary_product[2]
                            idx = self.get_idx(product_name)
                            current_product = self.element_amount[idx[0]][idx[1]][0]
                            if not can_be_negative and current_product < -negative_product_amount * product_amount:
                                self.produce_resource(product_name, -current_product)
                                self.element_amount[idx[0]][idx[1]][0] = 0
                            else:
                                self.produce_resource(product_name, negative_product_amount * product_amount)
                                self.element_amount[idx[0]][idx[1]][0] -= -negative_product_amount * product_amount
            # 4. Recalculate the values for all "机器" box.
            for produce_resource in self.sorted_element:
                i, j = self.get_idx(produce_resource)
                produce_resource_amount = self.element_amount[i][j][0]
                produce_speed = self.production[produce_resource][0][0]
                self.element_amount[i][j][1] = produce_resource_amount / produce_speed
            # update the window by new values.
            for i in range(len(self.element)):
                for j in range(len(self.element[0])):
                    if self.element[i][j] != '':
                        for k in range(4):
                            if k != 2 and k != 1:
                                amount = int(self.element_amount[i][j][k])
                            elif k == 1:
                                amount = round(self.element_amount[i][j][k], 2)
                            else:
                                amount = self.element_amount[i][j][k]
                            self.element_box[i][j][k].setText(str(amount))
        return update_table_inner

    def produce_resource(self, resource, increase_production_number):
        component = self.production[resource][1:]
        if not component:
            return

        for obj_resource in component:
            production_name = obj_resource[0]
            production_number = increase_production_number * obj_resource[1]
            i, j = self.get_idx(production_name)
            self.element_amount[i][j][0] += production_number
            produce_speed = self.production[production_name][0][0]
            self.element_amount[i][j][1] = self.element_amount[i][j][0] / produce_speed
            self.produce_resource(production_name, production_number)

    def ceil_machine_number(self):
        for idx in range(len(self.sorted_element)):
            resource = self.sorted_element[idx]
            i, j = self.get_idx(resource)
            if self.element_amount[i][j][0] < 0:
                pass
            else:
                current_machine_number = self.element_amount[i][j][1]
                obj_machine_number = ceil(current_machine_number)
                produce_speed = self.production[resource][0][0]
                obj_production_number = (obj_machine_number * produce_speed)
                increase_production_number = obj_production_number - self.element_amount[i][j][0]
                self.element_amount[i][j][0] = obj_production_number
                self.element_amount[i][j][1] = obj_machine_number
                if idx != len(self.sorted_element) - 1:
                    self.produce_resource(resource, increase_production_number)
        # update the window by new values.
        for i in range(len(self.element)):
            for j in range(len(self.element[0])):
                if self.element[i][j] != '':
                    for k in range(4):
                        amount = (self.element_amount[i][j][k])
                        self.element_box[i][j][k].setText(str(amount))

    def show(self):
        self.window.show()


