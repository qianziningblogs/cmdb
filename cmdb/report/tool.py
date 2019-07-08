import csv
import os


class SaveCsv(object):
    def __init__(self, objs, filename):
        '''
        :param objs: [[],[],]
        :param filename: str
        '''
        self.objs = objs
        self.filename = filename
        self.__save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'export_files')
        self.__save_path = os.path.join(self.__save_dir, self.filename)
    def save_to_file(self):
        os.system('mkdir -p {}'.format(self.__save_dir))
        with open(self.__save_path, 'w', encoding="utf-8-sig") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(self.objs)

    def deliver_to_backend(self):
        self.save_to_file()
        with open(self.__save_path, 'r') as f:
            for line in f:
                yield line


def read_file(file):
    with open(file, 'r') as f:
        for line in f:
            yield line

def test():
    import random
    objs = [obj for obj in zip(range(100), random.sample([str(i) + "item" for i in range(1, 101)], 100))]
    sh = SaveCsv(objs, 'test_csv_file')
    sh.save_to_file()


def deal_queryobject(queryset, filename, exclude=None):
    '''
    :param queryset: model QuerySet
    :param exclude:  要导出的字段
    :return:        可迭代对象
    '''
    exclude = exclude or []
    objs = []
    cols_name = []
    cols_name_finish = False
    for obj in queryset:
        obj_tmp = []
        for objf in obj._meta.get_fields():
            key = objf.name
            # print(type(objf))
            if key in exclude:
                continue
            if "reverse_related.Many" in str(type(objf)): # model作为其它model的外键时，不导出此属性
                continue
                
            # 有效col_name加入列表
            if not cols_name_finish:
                cols_name.append(key)
            
            value = getattr(obj, key)
            obj_tmp.append(value)
        
        if not cols_name_finish:
            objs.append(cols_name)
            cols_name_finish = True
        objs.append(obj_tmp)

    # save
    return SaveCsv(objs, filename).deliver_to_backend()


    

if __name__ == '__main__':
    test()