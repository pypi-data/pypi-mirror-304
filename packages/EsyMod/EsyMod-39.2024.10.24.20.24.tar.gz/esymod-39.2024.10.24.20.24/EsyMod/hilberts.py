import EsyPro
sfs = EsyPro.ScriptFileSaver(__file__, locals())

import torch

def hilbert_curve(n):
    def hilbert(x, y, xi, xj, yi, yj, n):
        if n <= 0:
            return [(x + (xi + yi) // 2, y + (xj + yj) // 2)]
        else:
            points = []
            points += hilbert(x, y, yi // 2, yj // 2, xi // 2, xj // 2, n - 1)
            points += hilbert(x + xi // 2, y + xj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            points += hilbert(x + xi // 2 + yi // 2, y + xj // 2 + yj // 2, xi // 2, xj // 2, yi // 2, yj // 2, n - 1)
            points += hilbert(x + xi // 2 + yi, y + xj // 2 + yj, -yi // 2, -yj // 2, -xi // 2, -xj // 2, n - 1)
            return points

    return hilbert(0, 0, 2**n, 0, 0, 2**n, n)


def hilbert_index_matrix(level=4):
    """
    生成希尔伯特整数矩阵
    :param dimensions: 维度
    :param bits: 每维度的位数
    :return: 希尔伯特整数矩阵
    """
    locations = hilbert_curve(level)
    matrix = torch.zeros(2**level, 2**level)
    for i, (x, y) in enumerate(locations):
        matrix[x, y] = i
    return matrix

class HilbertDecoder(torch.nn.Module):
    """
    希尔伯特解码，将输入序列解码为矩阵
    """
    def __init__(self, level=4):
        """
        初始化希尔伯特解码对象，指定级别。作用是将输入序列解码为矩阵
        参数:
            level (int, optional): 希尔伯特曲线的级别。默认值为4。
        属性:
            size (int): 希尔伯特曲线的级别。
            matrix (torch.Tensor): 指定级别的希尔伯特索引矩阵。
            seq_length (int): 序列长度，计算为4的level次方。
        """
        super().__init__()
        self.size = level
        self.matrix = hilbert_index_matrix(level).long()
        self.seq_length = 4**level
    
    def forward(self, x):
        """
        :param x: [torch.Tensor(seq_l, ...)]输入序列
        """
        # 如果序列长度不够，就自动补全
        if x.size(0) < self.seq_length:
            x = torch.cat(
                [
                    x,
                    torch.zeros(self.seq_length - x.size(0), *x.size()[1:], dtype=x.dtype, device=x.device)
                ]
            )
        
        x = x[self.matrix]
        # 把前两个维度移动到最后，保持其它维度不变
        dim_index = list(range(2, x.dim())) + [0, 1]
        x = x.permute(dim_index)
        # 如果维度个数小于4，则补充channel维度
        if x.dim() < 4:
            x = x.unsqueeze(-3)
        return x

class HilbertEncoder(torch.nn.Module):
    """
    希尔伯特编码，将输入矩阵编码为序列
    """
    def __init__(self, level):
        """
        初始化希尔伯特解码对象，指定级别。作用是将输入矩阵编码为序列
        参数:
            level (int, optional): 希尔伯特曲线的级别。默认值为4。
        属性:
            size (int): 希尔伯特曲线的级别。
            matrix (torch.Tensor): 指定级别的希尔伯特索引矩阵。
            seq_length (int): 序列长度，计算为4的level次方。
        """
        super().__init__()
        self.size = level
        self.matrix = hilbert_index_matrix(level).long()
        self.seq_length = 4**level
        
    def forward(self, x):
        """
        :param x: [torch.Tensor(..., H, W)]输入矩阵
        """
        # 把后两个维度移动到前面，保持其它维度不变
        dim_index = [-2, -1] + list(range(x.dim() - 2))
        x = x.permute(dim_index)
        
        # 根据矩阵索引，将矩阵转换为序列
        
        y = torch.zeros_like(x).flatten(0, 1)
        
        y[self.matrix] += x
        
        return y
        

    

if __name__ == '__main__':
    level = 8

    decoder = HilbertDecoder(level)
    
    line = torch.arange(2**(level*2)).view(-1, 1).expand(-1, 3).float()
    
    r = decoder(line)
    
    encoder = HilbertEncoder(level)
    
    r = encoder(r)
    
    sfs.end_script()
