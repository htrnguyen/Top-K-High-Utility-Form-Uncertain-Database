#!/usr/bin/env python
# coding: utf-8

# # Menu
# 
# 1. [**`# Top-K High-Utility Itemsets From Uncertain Databases`**](#top-k-high-utility-itemsets-from-uncertain-databases)
# 
# 2. [**`# Import libraries`**](#import-libraries)
# 3. [**`# Process Data`**](#process-data)
# 4. [**`# Algorithm ITUFP`**](#algorithm-itufp)
# 5. [**`# Main`**](#main)
# 

# ---
# 

# # Top-K High-Utility Itemsets From Uncertain Databases
# 
# **Mục tiêu**: Thuật toán tìm kiếm các **Top-K High Utility Itemsets** trong cơ sở dữ liệu không chắc chắn (Uncertain Database - UDB). Các itemsets này được chọn dựa trên giá trị hữu ích tổng thể và xác suất xảy ra của chúng.
# 
# ## Các Khái Niệm Cơ Bản
# 
# ### 1. **High Utility Itemset Mining (HUIS)**
# 
# **HUIS** là một lĩnh vực nghiên cứu trong khai phá dữ liệu, tập trung vào việc tìm kiếm các itemsets có giá trị **hữu ích** (utility) cao trong cơ sở dữ liệu giao dịch. Utility của một itemset được tính dựa trên các yếu tố như giá trị lợi nhuận của các mục và tần suất xuất hiện của chúng trong dữ liệu.
# 
# -   **Utility** của một itemset là tổng giá trị của các mục trong itemset đó, với giá trị của mỗi mục được tính dựa trên tần suất xuất hiện và lợi nhuận hoặc giá trị của mục đó trong các giao dịch.
# -   **High Utility Itemsets (HUIS)** là những itemsets có tổng utility vượt quá một ngưỡng tối thiểu (min-utility), thường được gọi là **min-utility threshold**.
# 
# Các bài toán HUIS rất quan trọng trong các ứng dụng như:
# 
# -   **Phân tích dữ liệu giao dịch**: Nhằm tìm các itemsets có giá trị cao nhất cho việc quảng bá sản phẩm hoặc phân tích hành vi khách hàng.
# -   **Hệ thống gợi ý sản phẩm**: Để gợi ý các sản phẩm hoặc mục có giá trị cao, được mua nhiều bởi người tiêu dùng.
# 
# ### 2. **Cơ Sở Dữ Liệu Không Chắc Chắn (Uncertain Database - UDB)**
# 
# Cơ sở dữ liệu không chắc chắn là một loại cơ sở dữ liệu trong đó thông tin có sự không chắc chắn, hay nói cách khác, các mục trong cơ sở dữ liệu có thể không xuất hiện trong tất cả các giao dịch với cùng một xác suất. Sự không chắc chắn này có thể phát sinh từ các yếu tố như:
# 
# -   **Dữ liệu không đầy đủ**: Một số mục có thể không được ghi lại trong cơ sở dữ liệu với độ chính xác hoàn hảo.
# -   **Dữ liệu thiếu xác suất**: Các mục trong cơ sở dữ liệu có thể có các xác suất khác nhau thay vì một giá trị xác định.
# 
# Một cơ sở dữ liệu không chắc chắn có thể chứa các thuộc tính sau:
# 
# -   **Items**: Các mục có thể xuất hiện trong giao dịch, nhưng không phải tất cả các mục đều có mặt trong tất cả các giao dịch.
# -   **Utility**: Giá trị của một mục trong giao dịch, có thể thay đổi dựa trên nhiều yếu tố khác nhau.
# -   **Probability**: Xác suất mà một mục sẽ xuất hiện trong một giao dịch nhất định.
# 
# Ví dụ, trong một cơ sở dữ liệu bán hàng, các mục có thể là các sản phẩm, và xác suất thể hiện khả năng khách hàng sẽ mua sản phẩm đó.
# 
# **Định nghĩa 1:** Mỗi item $x_i$ trong mỗi giao dịch $T_j$ có một xác suất tồn tại $P(x_i, T_j)$ $(0 < P(x_i, T_j) \leq 1)$.
# 
# **Định nghĩa 2:** Xác suất tồn tại của một mẫu X trong một giao dịch $T_j$ được xác định bằng cách:
# $$P(X, T_j) = \prod_{x \in X} P(x, T_j)$$
# 
# **Định nghĩa 3:** Chỉ số kỳ vọng (Expected support) của một mẫu X trong tập dữ liệu không chắc chắn kí hiệu là $expSup(X)$ và được xác định bằng:
# $$expSup(X) = \sum_{j = 1}^{|UDB|} (\prod_{x \in X} P(x, T_j)) = \sum_{j = 1}^{|UDB|} (P(X, T_j))$$
# 
# <!-- *Ví dụ:*  -->
# 
# **Giả thuyết 1:** Với mỗi $Y \subset X$, chỉ số kỳ vọng (expSup) thoả mãn các điều kiện sau:
# 
# -   Nếu $expSup(X) \geq minSup$ thì $expSup(Y) \geq minSup$.
# -   Nếu $expSup(Y) < minSup$ thì $expSup(X) < minSup$
# 
# **Problem statement.** Tập trung vào khai thác Top-K HUIs trên tập dữ liệu không chắc chắn với tiêu chí "xây dựng một lần, khai thác nhiều lần". Cho một tập dữ liệu không chắc chắn UDB và các giá trị K, vấn đề cần giải quyết là tìm kiếm K tập hợp có giá trị hữu ích cao nhất.
# 
# ### 3. **Top-K High Utility Itemset Mining (Top-K HUIs)**
# 
# Top-K High Utility Itemset Mining (Top-K HUIS) là một bài toán trong khai phá dữ liệu mà mục tiêu là tìm ra **K itemsets hữu ích cao nhất** từ cơ sở dữ liệu không chắc chắn, trong đó **K** là một tham số đầu vào được chỉ định.
# 
# -   Thuật toán sẽ tìm kiếm các itemsets có tổng giá trị hữu ích (utility) cao nhất trong cơ sở dữ liệu, chọn ra **K itemsets** có giá trị hữu ích cao nhất.
# -   Các itemsets này không chỉ được lựa chọn dựa trên tần suất xuất hiện mà còn dựa trên **giá trị hữu ích**, tức là sự kết hợp giữa xác suất và giá trị của các mục trong itemset.
# 
# ---
# 
# ## Cấu Trúc Thuật Toán
# 
# Thuật toán **ITUFP (Top-K High-Utility Itemset Mining)** hoạt động dựa trên cơ sở dữ liệu không chắc chắn và áp dụng các phương pháp khai phá để tìm ra các **Top-K High Utility Itemsets**.
# 
# #### Các bước chính của thuật toán:
# 
# 1. **Đọc và xử lý dữ liệu**: Thuật toán bắt đầu bằng việc đọc dữ liệu từ cơ sở dữ liệu không chắc chắn (UDB), trong đó mỗi giao dịch chứa các mục, giá trị hữu ích và xác suất của các mục.
# 2. **Tạo UPLists**: Thuật toán tạo các **UPLists**, là danh sách lưu trữ các mục trong cơ sở dữ liệu cùng với các giá trị hữu ích và xác suất của chúng.
# 3. **Khai thác các itemsets có giá trị hữu ích cao**: Thuật toán tìm kiếm các itemsets có giá trị hữu ích cao nhất và sắp xếp chúng theo thứ tự giảm dần.
# 4. **Top-K itemsets**: Dựa trên giá trị hữu ích và các chỉ số như xác suất, thuật toán sẽ chọn ra **K itemsets** có giá trị hữu ích cao nhất.
# 
# ### **Đánh giá**
# 
# Để đánh giá hiệu suất của thuật toán, chúng ta đo **thời gian chạy** và **bộ nhớ sử dụng**.
# 
# -   **Thời gian chạy**: Đo lường thời gian mà thuật toán cần để tìm kiếm các Top-K itemsets từ cơ sở dữ liệu không chắc chắn.
# -   **Bộ nhớ sử dụng**: Đo lường lượng bộ nhớ mà thuật toán yêu cầu trong suốt quá trình thực thi.
# 
# Các chỉ số này giúp người dùng hiểu được hiệu suất của thuật toán khi xử lý các cơ sở dữ liệu có kích thước khác nhau và các giá trị `k` khác nhau.
# 
# ---
# 
# ## Cấu Trúc Code Thuật Toán
# 
# 1. **Lớp `Transaction`**: Đại diện cho một giao dịch trong cơ sở dữ liệu không chắc chắn. Xem chi tiết trong phần [`Process Data`](#process-data).
# 2. **Lớp `UDB`**: Quản lý dữ liệu và chuyển đổi chúng thành các đối tượng `Transaction`. Xem chi tiết trong phần [`Process Data`](#process-data).
# 3. **Lớp `UPList`**: Đại diện cho một danh sách các mục (items) trong dữ liệu. Tham khảo chi tiết trong phần [`Algorithm ITUFP`](#algorithm-itufp).
# 4. **Lớp `IMCUPList`**: Đại diện cho các mẫu kết hợp được tạo ra từ các `UPList` hoặc `IMCUPList`. Tham khảo chi tiết trong phần [`Algorithm ITUFP`](#algorithm-itufp).
# 5. **Lớp `ITUFP`**: Triển khai thuật toán ITUFP để tìm các Top-K High Utility Itemsets. Tham khảo chi tiết trong phần [`Algorithm ITUFP`](#algorithm-itufp).
# 

# # Import libraries
# 

# In[36]:


import csv
import time
import os
import psutil
from typing import List, Dict, Any, Tuple, Generator
from collections import defaultdict
import matplotlib.pyplot as plt


# # Process Data
# 

# In[37]:


class Transaction:
    """Lớp đại diện cho một giao dịch trong dữ liệu không chắc chắn.

    Examples
    --------
    >>> transaction = Transaction(
    ...     id=1,
    ...     items=[1, 2, 3],
    ...     utilities=[10, 20, 30],
    ...     probabilities=[0.5, 0.3, 0.2]
    ... )
    >>> print(transaction)
    Transaction(1, [1, 2, 3], [10, 20, 30], [0.5, 0.3, 0.2])
    >>> transaction.to_dict()
    {
        'id': 1,
        'items': [1, 2, 3],
        'utilities': [10, 20, 30],
        'probabilities': [0.5, 0.3, 0.2]
    }
    """

    def __init__(
        self,
        id: int,
        items: List[int],
        utilities: List[float],
        probabilities: List[float],
    ) -> None:
        """Khởi tạo một giao dịch với id, items, utilities và probabilities cho mỗi item.

        Parameters
        ----------
        id : int
            Id của giao dịch.
        items : List[int]
            Danh sách các item trong giao dịch.
        utilities : List[float]
            Danh sách các giá trị của các item trong giao dịch.
        probabilities : List[float]
            Danh sách xác suất của các item trong giao dịch.
        """
        self.id = id
        self.items = items
        self.utilities = utilities
        self.probabilities = probabilities

    def to_dict(self) -> Dict[str, Any]:
        """Trả về giao dịch dưới dạng Dictionary.

        Returns
        -------
        Dict[str, Any]
            Dictionary chứa thông tin của giao dịch.
        """
        return {
            "id": self.id,
            "items": self.items,
            "utilities": self.utilities,
            "probabilities": self.probabilities,
        }

    def __repr__(self) -> str:
        """Trả về một chuỗi biểu diễn của đối tượng Transaction."""
        return f"Transaction({self.id}, {self.items}, {self.utilities}, {self.probabilities})"


# In[38]:


class UDB:
    """Lớp quản lý cơ sở dữ liệu không chắc chắn.

    Examples
    --------
    >>> udb = UDB("sample_data.csv")
    >>> transactions = udb.get_transactions()
    >>> for transaction in transactions:
    ...     print(transaction)
    [
        Transaction(1, [1, 2, 3], [10.0, 20.0, 30.0], [0.5, 0.3, 0.2]),
        Transaction(2, [1, 4], [10.0, 40.0], [0.6, 0.4]),
    ]
    """

    def __init__(self, file_path: str) -> None:
        """Khởi tạo một cơ sở dữ liệu không chắc chắn với đường dẫn file.

        Parameters
        ----------
        file_path : str
            Đường dẫn file chứa dữ liệu không chắc chắn.
        """
        self.file_path = file_path

    def read_file(self) -> Generator[Transaction, None, None]:
        """Đọc file và tạo Generator chứa các đối tượng Transaction.

        Returns
        -------
        Generator[Transaction, None, None]
            Generator chứa các đối tượng Transaction.
        """
        with open(self.file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for id, row in enumerate(csv_reader, start=1):
                try:
                    # Chuyển đổi các chuỗi thành danh sách
                    items = list(map(int, row["items"].split()))
                    utilities = list(map(float, row["item_utilities"].split()))
                    probabilities = list(map(float, row["item_probabilities"].split()))

                    # Kiểm tra tính hợp lệ
                    if len(items) != len(utilities) or len(items) != len(probabilities):
                        raise ValueError(
                            "The length of items, utilities, and probabilities must be the same."
                        )
                    if not all(0 <= p <= 1 for p in probabilities):
                        raise ValueError(
                            "The probabilities must be in the range [0, 1]."
                        )

                    # Trả về từng giao dịch dưới dạng Generator
                    yield Transaction(id, items, utilities, probabilities)
                except Exception as e:
                    print(f"Error at line {id}: {e}")

    def get_transactions(self) -> List[Transaction]:
        """Trả về một danh sách các giao dịch từ file.

        Returns
        -------
        List[Transaction]
            Danh sách các giao dịch.
        """
        return list(self.read_file())


# # Algorithm ITUFP
# 

# In[39]:


class UPList:
    """Lớp đại diện cho UP-List.

    Examples
    --------
    >>> uplist = UPList(item_name="1")
    >>> uplist.add_entry(tid=1, probability=0.5, utility=10)
    >>> uplist.add_entry(tid=2, probability=0.3, utility=20)
    >>> uplist.add_entry(tid=3, probability=0.2, utility=30)
    >>> print(uplist)
    UPList(1: [(1, 0.5, 10), (2, 0.3, 20), (3, 0.2, 30)], Total Utility: 60.0, Expected Support: 1.0)
    """

    def __init__(self, item_name: str) -> None:
        """Khởi tạo UPList

        Parameters
        ----------
        item_name : str
            Tên của mục.
        """
        self.item_name: str = item_name
        # List các entry (tid, probability, utility)
        self.entries: List[Tuple[int, float, float]] = []
        self.total_utility: float = 0.0
        self.exp_support: float = 0.0

    def add_entry(self, tid: int, probability: float, utility: float) -> None:
        """Thêm một entry vào UP-List.

        Parameters
        ----------
        tid : int
            ID của giao dịch.
        probability : float
            Xác suất của mục trong giao dịch.
        utility : float
            Giá trị hữu ích của mục trong giao dịch.
        """
        self.entries.append((tid, probability, utility))
        self.total_utility += utility
        self.exp_support += probability

    def __repr__(self) -> str:
        """Trả về chuỗi đại diện cho UP-List.

        Returns
        ----------
        str
            Chuỗi đại diện cho UP-List.
        """
        return (
            f"UPList({self.item_name}: {self.entries}, "
            f"Total Utility: {self.total_utility}, "
            f"Expected Support: {self.exp_support})"
        )


# In[40]:


class UplistManager:
    """Lớp quản lý các UPLists, hỗ trợ truy xuất và xử lý."""

    def __init__(self, up_lists: List[UPList]) -> None:
        """Khởi tạo UplistManager với danh sách UPList."""
        self.up_lists = up_lists

    def get_uplist(self, item_name: int) -> UPList:
        """Lấy UPList theo tên mục.

        Parameters
        ----------
        item_name : int
            Tên của mục (item_name).

        Returns
        -------
        UPList
            UPList tương ứng với item_name.
        """
        for uplist in self.up_lists:
            if uplist.item_name == item_name:
                return uplist
        raise ValueError(f"UPList with item_name {item_name} not found.")


# In[41]:


class IMCUPList:
    """Lớp đại diện cho IMCUP-List, lưu trữ các mẫu kết hợp và utilities của chúng.

    Examples
    --------
    >>> uplist_1 = UPList(item_name="1")
    >>> uplist_1.add_entry(tid=1, probability=0.5, utility=10)
    >>>
    >>> uplist_2 = UPList(item_name="2")
    >>> uplist_2.add_entry(tid=1, probability=0.6, utility=15)
    >>>
    >>> uplist_3 = UPList(item_name="3")
    >>> uplist_3.add_entry(tid=1, probability=0.7, utility=20)
    >>>
    >>> imcup_list_12 = IMCUPList(pattern_name="1,2")
    >>> imcup_list_12.construct(uplist_1, uplist_2, prefix_indices=[], uplist_manager=uplist_manager)
    >>>
    >>> imcup_list_13 = IMCUPList(pattern_name="1,3")
    >>> imcup_list_13.construct(uplist_1, uplist_3, prefix_indices=[], uplist_manager=uplist_manager)
    >>>
    >>> print(imcup_list_12)
    IMCUPList(1,2: [(1, 0.3, 25.0)], Total Utility: 25.0, Expected Support: 0.3)
    >>>
    >>> print(imcup_list_13)
    IMCUPList(1,3: [(1, 0.35, 30.0)], Total Utility: 30.0, Expected Support: 0.35)

    >>> imcup_list_123 = IMCUPList(pattern_name="1,2,3")
    >>> imcup_list_123.construct(imcup_list_12, imcup_list_13, prefix_indices=[1], uplist_manager=uplist_manager)
    >>> print(imcup_list_123)
    IMCUPList(1,2,3: [(1, 0.21, 45.0)], Total Utility: 45.0, Expected Support: 0.21)
    """

    def __init__(self, pattern_name: str) -> None:
        """Khởi tạo IMCUP-List với tên mẫu."""
        self.pattern_name: str = pattern_name
        # List các entry (tid, probability, utility)
        self.entries: List[Tuple[int, float, float]] = []
        self.total_utility: float = 0.0
        self.exp_support: float = 0.0

    def construct(
        self,
        list1: UPList or "IMCUPList",  # type: ignore
        list2: UPList or "IMCUPList",  # type: ignore
        prefix_indices: List[int],
        uplist_manager: List[UPList],
    ) -> None:
        """
        Tạo IMCUP-List bằng cách kết hợp hai danh sách (IMCUPList hoặc UPList).

        Parameters
        ----------
        list1 : IMCUPList or UPList
            Danh sách đầu tiên.
        list2 : IMCUPList or UPList
            Danh sách thứ hai.
        prefix_indices : List[int]
            Danh sách các chỉ số của các mục cần làm tiền tố.
        uplist_manager : UPListManager
            Lớp quản lý UPLists.
        """
        idx1, idx2 = 0, 0

        # Lấy danh sách UPLists của các tiền tố (nếu có)
        prefix_lists = [uplist_manager.get_uplist(idx) for idx in prefix_indices]

        while idx1 < len(list1.entries) and idx2 < len(list2.entries):
            tid1, prob1, util1 = list1.entries[idx1]
            tid2, prob2, util2 = list2.entries[idx2]

            if tid1 == tid2:  # Nếu cùng giao dịch (TID)
                combined_prob = prob1 * prob2
                combined_util = util1 + util2

                # Loại bỏ utility trùng lặp từ các tiền tố
                for prefix_list in prefix_lists:
                    for tid_prefix, prob_prefix, util_prefix in prefix_list.entries:
                        if tid_prefix == tid1:
                            combined_prob /= prob_prefix
                            combined_util -= util_prefix
                            break

                # Cập nhật vào IMCUPList
                self.entries.append((tid1, combined_prob, combined_util))
                self.total_utility += combined_util
                self.exp_support += combined_prob

                idx1 += 1
                idx2 += 1
            elif tid1 < tid2:
                idx1 += 1
            else:
                idx2 += 1

    def __repr__(self) -> str:
        """Trả về chuỗi đại diện cho IMCUP-List.

        Returns
        -------
        str
            Chuỗi đại diện cho IMCUP-List.
        """
        return (
            f"IMCUPList({self.pattern_name}: {self.entries}, "
            f"Total Utility: {self.total_utility}, "
            f"Expected Support: {self.exp_support})"
        )


# In[42]:


class ITUFP:
    """Thuật toán ITUFP để khai thác Top-K High-Utility Itemsets từ cơ sở dữ liệu không chắc chắn.

    Examples
    --------
    >>> udb = UDB("sample_data.csv")
    >>> itufp = ITUFP(udb, k=2)
    >>> top_k_itemsets = itufp.run()
    >>> print(top_k_itemsets)
    [
        ('1', 60.0, 1.5),
        ('1,2', 25.0, 0.3)
    ]
    """

    def __init__(self, udb: UDB, k: int):
        """Khởi tạo đối tượng ITUFP.

        Parameters
        -----------
        udb : UDB
            Cơ sở dữ liệu không chắc chắn.
        k : int
            Số lượng Top-K High-Utility Itemsets cần tìm.
        """

        self.udb: UDB = udb
        self.k: int = k
        self.top_k: List[Tuple[str, float, float]] = []
        self.min_sup: float = 0.0

        # Tạo danh sách UPLists
        self.uplist_manager: UplistManager = self.generate_up_lists()
        self._pattern_indices = {}

    def generate_up_lists(self) -> UplistManager:
        """Tạo danh sách UPLists từ cơ sở dữ liệu UDB và sắp xếp theo expSupport (giảm dần).

        Returns
        -------
        UplistManager
            Lớp quản lý UPLists.
        """

        up_lists = defaultdict(lambda: UPList(item_name=""))

        for transaction in self.udb.get_transactions():
            for item, prob, util in zip(
                transaction.items, transaction.probabilities, transaction.utilities
            ):
                if not up_lists[item].item_name:
                    up_lists[item].item_name = item
                up_lists[item].add_entry(transaction.id, prob, util)

        return UplistManager(
            sorted(up_lists.values(), key=lambda x: x.exp_support, reverse=True)
        )

    def find_prefix_indices(self, pattern1: str, pattern2: str) -> List[int]:
        """Tìm danh sách các mục tiền tố trùng lặp giữa hai mẫu.

        Parameters
        ----------
        pattern1 : str
            Tên của mẫu thứ nhất.
        pattern2 : str
            Tên của mẫu thứ hai.

        Returns
        -------
        List[int]
            Danh sách các mục trùng lặp theo thứ tự xuất hiện.
        """
        key = f"{pattern1}_{pattern2}"
        if key not in self._pattern_indices:
            items1 = tuple(map(int, pattern1.split(",")))
            items2 = tuple(map(int, pattern2.split(",")))
            self._pattern_indices[key] = [item for item in items1 if item in items2]
        return self._pattern_indices[key]

    def mine_patterns(self, uplist_manager: UplistManager) -> None:
        """Đệ quy khai thác các tổ hợp từ UPLists và IMCUPLists.

        Parameters
        ----------
        uplist_manager : UplistManager
            Lớp quản lý UPLists.
        """

        imcup_lists = []
        up_lists = uplist_manager.up_lists

        # Lọc các UPLists có expSupport > minSup
        valid_indices = [
            i for i, up in enumerate(up_lists) if up.exp_support > self.min_sup
        ]

        # Tạo IMCUPLists từ các cặp UPLists
        for i in valid_indices:
            for j in range(i + 1, len(valid_indices)):
                idx_j = valid_indices[j]

                # Early pruning cho cặp items
                if (
                    up_lists[i].exp_support * up_lists[idx_j].exp_support
                    <= self.min_sup
                ):
                    continue

                imcup = IMCUPList(
                    f"{uplist_manager.up_lists[i].item_name},{uplist_manager.up_lists[j].item_name}"
                )

                imcup.construct(
                    uplist_manager.up_lists[i],
                    uplist_manager.up_lists[j],
                    [],
                    uplist_manager,
                )

                if imcup.exp_support <= self.min_sup:
                    continue

                imcup_lists.append(imcup)

                self._update_top_k(imcup)

        if imcup_lists:
            self.itufp_growth(imcup_lists, uplist_manager)

    def _update_top_k(self, item):
        pattern_name = item.item_name if isinstance(item, UPList) else item.pattern_name
        entry = (pattern_name, item.total_utility, item.exp_support)

        self.top_k.append(entry)
        self.top_k.sort(key=lambda x: x[1], reverse=True)

        if len(self.top_k) > self.k:
            self.top_k.pop()
            self.min_sup = self.top_k[-1][2]

    def itufp_growth(
        self,
        imcup_lists: List[IMCUPList],
        uplist_manager: UplistManager,
    ) -> None:
        """Đệ quy mở rộng khai thác các tổ hợp dài hơn từ IMCUPLists.

        Parameters
        ----------
        imcup_lists : List[IMCUPList]
            Danh sách các IMCUPLists cần mở rộng.
        uplist_manager : UplistManager
            Lớp quản lý UPLists.
        """

        next_level = []

        # Early pruning với min_sup
        valid_imcups = [
            imcup for imcup in imcup_lists if imcup.exp_support > self.min_sup
        ]

        for i, imcup1 in enumerate(valid_imcups):
            prefix1 = tuple(imcup1.pattern_name.split(",")[:-1])

            for imcup2 in valid_imcups[i + 1 :]:
                if tuple(imcup2.pattern_name.split(",")[:-1]) != prefix1:
                    continue

                new_pattern_name = (
                    f"{imcup1.pattern_name},{imcup2.pattern_name.split(',')[-1]}"
                )

                new_imcup = IMCUPList(new_pattern_name)

                # Tìm prefix indices
                prefix_indices = self.find_prefix_indices(
                    imcup1.pattern_name, imcup2.pattern_name
                )

                new_imcup.construct(imcup1, imcup2, prefix_indices, uplist_manager)

                if new_imcup.exp_support <= self.min_sup:
                    continue

                next_level.append(new_imcup)

                self._update_top_k(new_imcup)

        if next_level:
            self.itufp_growth(next_level, uplist_manager)

    def run(self) -> List[Tuple[str, float, float, float]]:
        """Chạy thuật toán ITUFP để tìm Top-K High-Utility Itemsets.

        Returns
        -------
        List[Tuple[str, float, float, float]]
            Danh sách các High-Utility Itemsets với tên, tổng utility, expSupport và minSup.
        """

        # Khai thác 1-itemsets
        valid_uplists = [
            up for up in self.uplist_manager.up_lists if up.exp_support > self.min_sup
        ]

        for uplist in valid_uplists:
            self._update_top_k(uplist)

        # Khai thác các tổ hợp dài hơn
        self.mine_patterns(self.uplist_manager)

        return self.top_k


# # Main
# 

# In[43]:


def save_results_to_file(
    file_path: str,
    results: List[Tuple[str, float, float]],
    k: int,
    elapsed_time: float,
    memory_usage: float,
) -> None:
    """
    Lưu kết quả Top-K High-Utility Itemsets vào tệp .txt.

    Parameters:
    ----------
    file_path : str
        Đường dẫn tệp đầu ra.
    results : List[Tuple[str, float, float]]
        Kết quả Top-K High-Utility Itemsets.
    k : int
        Số lượng Top-K High-Utility Itemsets cần lưu.
    elapsed_time : float
        Thời gian chạy thuật toán.
    memory_usage : float
        Bộ nhớ sử dụng khi chạy thuật toán.
    """
    with open(file_path, "w") as f:
        f.write("Results of ITUFP Algorithm\n")
        f.write("=" * 50 + "\n")
        f.write(f"Top-{k} High-Utility Itemsets:\n")
        f.write("=" * 50 + "\n")
        for idx, (itemset, total_utility, exp_support) in enumerate(results, start=1):
            f.write(
                f"{idx}. Itemset: {itemset} | Total Utility: {total_utility:.2f} | "
                f"Expected Support: {exp_support:.2f}\n"
            )
        f.write("=" * 50 + "\n")
        f.write(f"Execution Time: {elapsed_time:.2f} seconds\n")
        f.write(f"Memory Usage: {memory_usage:.2f} MB\n")
        f.write("=" * 50 + "\n")


def main(file_path: str, k: int = 20) -> None:
    """Chạy thuật toán ITUFP và in kết quả Top-K High-Utility Itemsets từ cơ sở dữ liệu UDB.

    Parameters:
    ----------
    file_path : str
        Đường dẫn đến tệp dữ liệu.
    k : int, optional
        Số lượng Top-K High-Utility Itemsets cần tìm, mặc định là 20.
    """

    # Tạo đối tượng UDB từ file path
    udb = UDB(file_path)

    # Đo thời gian và bộ nhớ trước khi chạy thuật toán
    start_time = time.time()
    process = psutil.Process()
    memory_before = process.memory_info().rss / (1024 * 1024)

    # Tạo đối tượng ITUFP và chạy thuật toán
    itufp = ITUFP(udb, k)
    results = itufp.run()

    # Đo thời gian và bộ nhớ sau khi chạy thuật toán
    end_time = time.time()
    memory_after = process.memory_info().rss / (1024 * 1024)
    elapsed_time = end_time - start_time
    memory_usage = memory_after - memory_before

    # In kết quả Top-K High-Utility Itemsets
    print("==" * 40)
    print("Top-K High-Utility Itemsets:")
    for idx, (itemset, total_utility, exp_support) in enumerate(results, start=1):
        print(
            f"{idx}. Itemset: {itemset} | Total Utility: {total_utility:.2f} | "
            f"Expected Support: {exp_support:.2f}"
        )

    # In thời gian chạy và bộ nhớ sử dụng
    print(f"\nExecution Time: {elapsed_time:.2f} seconds")
    print(f"Memory Usage: {memory_usage:.2f} MB")

    # Lưu kết quả vào file
    file_name = os.path.basename(file_path).split(".")[0] + "_results.txt"
    save_results_to_file(file_name, results, k, elapsed_time, memory_usage)
    print(f"Results saved to {file_name}")


# ## Kiểm tra với tập mẫu
# 

# In[44]:


file_path = "./Uncertain_DB/sample_data.csv"
main(file_path, k=20)


# ## Kiểm tra với tập Chess
# 

# In[52]:


file_path = "./Uncertain_DB/processed_chess_utility_spmf.csv"
main(file_path, k=300)


# ## Kiểm tra trên tập FoodMart
# 

# In[53]:


file_path = "./Uncertain_DB/processed_foodmart.csv"
main(file_path, k=300)


# ## Kiểm tra với tập Retail
# 

# In[47]:


file_path = "./Uncertain_DB/processed_retail_utility_spmf.csv"
main(file_path, k=10)


# ## Kiểm tra với tập Connect
# 

# In[48]:


# file_path = "./Uncertain_DB/processed_connect_utility_spmf.csv"
# main(file_path, k=50)


# ## Trực quan dữ liệu
# 

# In[49]:


# def measure_time(udb: UDB, k: int) -> Tuple[float, float]:
#     """Đo thời gian khi chạy thuật toán ITUFP với giá trị k.

#     Parameters:
#     ----------
#     udb : UDB
#         Cơ sở dữ liệu UDB.
#     k : int
#         Số lượng Top-K High-Utility Itemsets cần tìm.

#     Returns:
#     -------
#     Tuple[float, float]
#         Thời gian thực thi (giây).
#     """
#     start_time = time.time()

#     # Chạy thuật toán ITUFP
#     itufp = ITUFP(udb, k)
#     itufp.run()

#     # Đo thời gian sau khi chạy thuật toán
#     end_time = time.time()
#     elapsed_time = end_time - start_time  # Thời gian chạy (giây)

#     return elapsed_time


# def compare_algorithms(file_paths: List[str], k_values: List[int]) -> None:
#     """So sánh thời gian khi chạy thuật toán ITUFP với nhiều file và giá trị k khác nhau.

#     Parameters:
#     ----------
#     file_paths : List[str]
#         Danh sách các đường dẫn tệp dữ liệu.
#     k_values : List[int]
#         Danh sách các giá trị k để thử nghiệm.
#     """
#     # Chuẩn bị các kết quả để vẽ biểu đồ
#     time_results = {file: [] for file in file_paths}

#     # So sánh trên mỗi tệp và với các giá trị k khác nhau
#     for file_path in file_paths:
#         print(f"Running for file: {file_path}")
#         udb = UDB(file_path)

#         for k in k_values:
#             print(f"  Running for k = {k}...")
#             time_taken = measure_time(udb, k)
#             time_results[file_path].append(time_taken)

#     # Vẽ biểu đồ thời gian chạy
#     plt.figure(figsize=(10, 6))

#     for file_path in file_paths:
#         plt.plot(k_values, time_results[file_path], label=f"Time for {file_path}")

#     plt.xlabel("k (Top-K)")
#     plt.ylabel("Time (seconds)")
#     plt.title("Execution Time vs k (Top-K) for ITUFP Algorithm")
#     plt.legend()
#     plt.grid(True)
#     plt.show()


# # Gọi hàm so sánh với các tệp dữ liệu và giá trị k
# file_paths = [
#     "./Uncertain_DB/processed_foodmart.csv",
#     "./Uncertain_DB/processed_chess_utility_spmf.csv",
# ]
# k_values = [10, 20, 50, 100, 200, 300]

# compare_algorithms(file_paths, k_values)

