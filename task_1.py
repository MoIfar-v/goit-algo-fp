class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data):
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        elems = []
        current = self.head
        while current:
            elems.append(str(current.data))
            current = current.next
        if elems:
            print(" -> ".join(elems))
        else:
            print("Порожній список")

    def reverse(self) -> None:
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev
        
    def sort(self) -> None:
        """Відсортувати зв'язний список."""
        self.head = merge_sort(self.head)


def merge(a: Node | None, b: Node | None) -> Node | None:
    """Злити два відсортовані списки вузлів і повернути голову нового списку.
    """
    dummy = Node()
    tail = dummy
    pa, pb = a, b
    while pa and pb:
        if pa.data <= pb.data:
            tail.next = pa
            pa = pa.next
        else:
            tail.next = pb
            pb = pb.next
        tail = tail.next
    tail.next = pa or pb
    return dummy.next


def _split(head):
    """Розділити список на дві половини."""
    if head is None or head.next is None:
        return head, None
    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    return head, mid


def merge_sort(head: Node | None) -> Node | None:
    """Рекурсивне сортування злиттям для списку."""
    if head is None or head.next is None:
        return head
    left, right = _split(head)
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


def merge_two_sorted_lists(l1: 'LinkedList', l2: 'LinkedList') -> 'LinkedList':
    """Дано два відсортовані LinkedList — повернути новий відсортований LinkedList."""
    merged = LinkedList()
    merged.head = merge(l1.head, l2.head)
    return merged


if __name__ == '__main__':

    l = LinkedList()
    for v in [3, 1, 4, 2, 5]:
        l.insert_at_end(v)

    print("Початковий список:")
    l.print_list()

    # Реверс
    l.reverse()
    print("Після реверсу:")
    l.print_list()

    # Сортування
    l.sort()
    print("Після сортування:")
    l.print_list()

    # Злиття двох відсортованих списків
    a = [1, 3, 5]
    a_ll = LinkedList()
    for v in a:
        a_ll.insert_at_end(v)

    b = [2, 4, 6, 8]
    b_ll = LinkedList()
    for v in b:
        b_ll.insert_at_end(v)

    print(f"Список A (відсортований): {a}")
    print(f"Список B (відсортований): {b}")

    merged = merge_two_sorted_lists(a_ll, b_ll)
    print(f"Злитий список:")
    merged.print_list()

