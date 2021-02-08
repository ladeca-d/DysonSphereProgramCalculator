from PySide2.QtWidgets import QPushButton, QMainWindow, QLabel, QLineEdit, QGroupBox
from math import ceil
import source


class MainWindow(QMainWindow):
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
        self.line_edit_font_size = self.font_size * 0.9 * 0.75
        self.element = source.element
        self.production = source.production
        self.supporter = source.support
        self.bi_material = source.bi_material
        self.sorted_element = source.sorted_element
        self.element_box = [[[None, None, None, None] for _ in range(len(self.element[0]))] for _ in range(len(self.element))]
        self.element_amount = [[[0, 0, 0, 0] for _ in range(len(self.element[0]))] for _ in range(len(self.element))]
        self.table_gen()
        for resource in self.sorted_element:
            i, j = self.get_idx(resource)
            for k in range(4):
                self.element_box[i][j][k].editingFinished.connect(self.update_element_amount)

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

        return [product00, product01, product10, product11]

    # update the window by the values of the self.element_amount.
    def update_view(self, is_int=[True, False, True, True]):
        for resource in self.sorted_element:
            i, j = self.get_idx(resource)
            for k in range(4):
                amount = round(self.element_amount[i][j][k], 1)
                if is_int[k]:
                    amount = int(self.element_amount[i][j][k])
                self.element_box[i][j][k].setText(str(amount))

    def get_idx(self, resource):
        idx = None
        if resource != '':
            for i in range(len(self.element)):
                for j in range(len(self.element[0])):
                    if resource == self.element[i][j]:
                        idx = [i, j]
        return idx

    def produce_resource(self, resource, increase_production_number):
        # Add resource amount in self.element_amount.
        idx = self.get_idx(resource)
        if not idx:
            exit(1)
        else:
            i, j = idx
            self.element_amount[i][j][0] += increase_production_number
            production_speed = self.production[resource][0][0]
            self.element_amount[i][j][1] += increase_production_number / production_speed

        # Start to product required amount of the resource.
        component = self.production[resource][1:]
        if not component:
            return

        for obj_resource in component:
            production_name = obj_resource[0]
            production_number = increase_production_number * obj_resource[1]
            self.produce_resource(production_name, production_number)

    def calculate_supporter(self):
        for supporter, properties in self.supporter.items():
            i, j = self.get_idx(supporter)
            amount = self.element_amount[i][j][3]
            for production in properties:
                i, j = self.get_idx(production[0])
                production_amount = self.element_amount[i][j][0]
                convert_amount_to_production_amount = amount * production[1]
                need_negative_production = convert_amount_to_production_amount - production_amount
                if need_negative_production > 0:
                    self.produce_resource(production[0], -1 * production_amount)
                else:
                    self.produce_resource(production[0],  -1 * convert_amount_to_production_amount)

    def calculate_bi_raw_material(self):
        # Calculate the need of the bi_raw_materials.
        for material, properties in self.bi_material.items():
            # production1
            production1 = properties[0][0]
            i, j = self.get_idx(production1)
            production1_amount = properties[0][1]
            need_production1_amount = self.element_amount[i][j][0]
            need_material_amount1 = need_production1_amount / production1_amount
            # production2
            production2 = properties[1][0]
            i, j = self.get_idx(production2)
            production2_amount = properties[1][1]
            need_production2_amount = self.element_amount[i][j][0]
            need_material_amount2 = need_production2_amount / production2_amount

            # Calculate the need of the material
            need_material_amount = max(need_material_amount1, need_material_amount2)
            i, j = self.get_idx(material)
            self.element_amount[i][j][0] = need_material_amount
            material_production_speed = self.production[material][0][0]
            self.element_amount[i][j][1] = need_material_amount / material_production_speed

    def update_element_amount(self, has_supporter=True):
        # Read all LineEdit boxes.
        for resource in self.sorted_element:
            i, j = self.get_idx(resource)
            for k in range(4):
                input_value = self.element_box[i][j][k].text()
                if k == 0 or k == 1 or input_value == '':
                    self.element_amount[i][j][k] = 0.0
                else:
                    self.element_amount[i][j][k] = float(input_value)

        # Produce the required amount of all resources.
        for resource in self.sorted_element:
            i, j = self.get_idx(resource)
            production_amount = self.element_amount[i][j][2] - self.element_amount[i][j][3]
            if production_amount < 0:
                self.produce_resource(resource, 0)
            else:
                self.produce_resource(resource, production_amount)

        # Calculate the second product of the special supporter.
        if has_supporter:
            self.calculate_supporter()
        # Calculate the need of the bi_raw_material.
        self.calculate_bi_raw_material()
        # Update the view of the app.
        self.update_view()

    def ceil_machine_number(self):
        # Re-update element amount without considering supporter.
        self.update_element_amount(False)

        # Calculate supporter.
        supporter_stack = dict()
        for support, products in self.supporter.items():
            i, j = self.get_idx(support)
            support_amount = self.element_amount[i][j][3]
            for product in products:
                product_name = product[0]
                product_amount = product[1]
                supporter_stack[product_name] = support_amount * product_amount

        # Ceil machine amount and produce the required amount of the resources.
        for resource in self.sorted_element:
            if resource not in self.supporter:
                i, j = self.get_idx(resource)
                production_speed = self.production[resource][0][0]
                if resource in supporter_stack:
                    cur_resource_amount = self.element_amount[i][j][0]
                    real_resource_amount = cur_resource_amount - supporter_stack[resource]
                    if real_resource_amount > 0:
                        cur_machine_amount = real_resource_amount / production_speed
                        new_machine_amount = ceil(cur_machine_amount)
                    else:
                        new_machine_amount = 0
                else:
                    cur_machine_amount = self.element_amount[i][j][1]
                    new_machine_amount = ceil(cur_machine_amount)
                    cur_resource_amount = self.element_amount[i][j][0]
                incre_resource_amount = new_machine_amount * production_speed - cur_resource_amount
                self.produce_resource(resource, incre_resource_amount)
                self.element_amount[i][j][1] = new_machine_amount

        # Calculate the need of the bi_raw_material.
        self.calculate_bi_raw_material()
        # Update the view of the app.
        # Production amount is allowed to be float since its unit is piece/min.
        self.update_view([False, True, True, True])

    def show(self):
        self.window.show()

