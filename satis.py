import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Faylı oxuyaq
df = pd.read_csv("satislar_data.csv")
# print(df)

# Endirim dərəcələrinə görə satılan məhsul miqdarını hesablayaq
discount_impact = df.groupby('discount_pct')['quantity'].sum()
# print(discount_impact)

# Həftənin günlərinə görə satışlar
weekday_sales = df.groupby('weekday')['total_amount'].sum()
# print(weekday_sales)

# Saatlara görə satışlar
hourly_sales = df.groupby('hour')['total_amount'].sum()
# print(hourly_sales)

# Kateqoriyalara görə satış miqdarı və məbləği
category_quantity = df.groupby('product_category')['quantity'].sum().sort_values(ascending=False)
category_revenue = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
# print(category_quantity)
# print(category_revenue)

# VIP və adi müştərilərin müqayisəsi
vip_analysis = df.groupby('is_vip_customer').agg({
    'total_amount': ['sum', 'mean'],
    'sale_id': 'count',
    'customer_id': 'nunique'
})
# print(vip_analysis)

# Əgər qaytarma məlumatları varsa
if 'is_returned' in df.columns:
    # Ümumi qaytarma dərəcəsi
    return_rate = df['is_returned'].mean() * 100

    # Qaytarma səbəbləri
    return_reasons = df[df['is_returned'] == True]['return_reason'].value_counts()

    # Ən çox qaytarılan məhsullar
    product_return_rates = df.groupby('product_name')['is_returned'].mean().sort_values(ascending=False) * 100
# print(return_rate)
# print(return_reasons)
# print(product_return_rates)

# Kateqoriya və endirim dərəcəsinə görə satış analizi
cat_discount_analysis = df.pivot_table(
    index='product_category',
    columns='discount_pct',
    values='quantity',
    aggfunc='sum',
    fill_value=0
)
# # print(cat_discount_analysis)


# Qrafiklərin daha gözəl görünməsi üçün
plt.style.use('seaborn-v0_8-whitegrid') 
sns.set(font_scale=1.2)

# Tarix sütununu düzgün formata çevirək
df['date'] = pd.to_datetime(df['date'])

# Endirim səviyyələrinə görə satılan məhsul sayı
discount_impact = df.groupby('discount_pct')['quantity'].sum()

plt.figure(figsize=(10, 6))
discount_impact.plot(kind='bar', color='skyblue')
plt.title('Endirim Səviyyələrinə görə Satılan Məhsul Sayı', fontsize=14)
plt.xlabel('Endirim Dərəcəsi')
plt.ylabel('Satılan Məhsul Sayı')
plt.xticks(rotation=0)  # Oxunması daha rahat olsun deyə etiketləri fırlatmırıq
plt.grid(axis='y', alpha=0.3)

# Hər sütunda dəyərləri göstərək
for i, v in enumerate(discount_impact):
    plt.text(i, v + 50, f"{v}", ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

# Ən çox satılan məhsullar
top_products = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(12, 6))
ax = top_products.plot(kind='barh', color='salmon')
plt.title('Ən Çox Satılan 5 Məhsul', fontsize=14)
plt.xlabel('Satış Sayı')
plt.ylabel('Məhsul')

# Sütun dəyərlərini göstərək
for i, v in enumerate(top_products):
    plt.text(v + 10, i, f"{v}", va='center')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# Aylıq satışları hesablayaq
monthly_sales = df.groupby(pd.Grouper(key='date', freq='M'))['total_amount'].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['date'], monthly_sales['total_amount'], marker='o', linestyle='-', linewidth=2, color='#2E86C1')
plt.title('Aylıq Satış Trendi', fontsize=14)
plt.xlabel('Tarix')
plt.ylabel('Ümumi Satış Məbləği')
plt.grid(True, alpha=0.3)

# Pik nöqtələri işarələyək
peak_month = monthly_sales.loc[monthly_sales['total_amount'].idxmax()]
plt.scatter(peak_month['date'], peak_month['total_amount'], s=100, color='red')
plt.annotate(f"Pik: {peak_month['date'].strftime('%B %Y')}",
             (peak_month['date'], peak_month['total_amount']),
             textcoords="offset points", xytext=(0,10), ha='center')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Saat üzrə satışlar
hourly_sales = df.groupby('hour')['total_amount'].sum()

plt.figure(figsize=(12, 6))
hourly_sales.plot(kind='line', marker='o', color='#8E44AD', linewidth=2)
plt.title('Saat üzrə Satışlar', fontsize=14)
plt.xlabel('Saat')
plt.ylabel('Ümumi Satış Məbləği')
plt.xticks(range(24))  # 24 saat üçün
plt.grid(True, alpha=0.3)

# Pik saatları işarələyək
peak_hours = hourly_sales.nlargest(2)
for hour, amount in peak_hours.items():
    plt.annotate(f"Pik: Saat {hour}",
                 (hour, amount),
                 textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()

# Kateqoriyalara görə satış məbləği
category_sales = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
top_categories = category_sales.head(5)
other_categories = pd.Series({'Digər': category_sales[5:].sum()})
pie_data = pd.concat([top_categories, other_categories])

plt.figure(figsize=(10, 8))
plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%',
        startangle=90, shadow=False,
        colors=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6', '#95A5A6'])

# Başlıq əlavə edək və dairə şəklində olmasını təmin edək
plt.title('Məhsul Kateqoriyalarının Ümumi Satışda Payı', fontsize=14)
plt.axis('equal')  # Dairə şəklində olması üçün
plt.tight_layout()
plt.show()

# Ödəniş metodlarına görə satışlar
payment_methods = df.groupby('payment_method')['total_amount'].sum()

plt.figure(figsize=(10, 8))
plt.pie(payment_methods, labels=payment_methods.index, autopct='%1.1f%%',
        startangle=90, explode=[0.05]*len(payment_methods),
        colors=sns.color_palette('pastel'))
plt.title('Ödəniş Metodlarının Payı', fontsize=14)
plt.axis('equal')
plt.tight_layout()
plt.show()

# Həftənin günü və saata görə satışlar
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hour_day_sales = df.pivot_table(index='weekday', columns='hour',
                                values='total_amount', aggfunc='sum')
hour_day_sales = hour_day_sales.reindex(weekday_order)  # Günləri düzgün sıralayaq

plt.figure(figsize=(14, 8))
sns.heatmap(hour_day_sales, cmap='YlGnBu', annot=False, linewidths=.5)
plt.title('Həftənin Günləri və Saatlara görə Satışlar', fontsize=14)
plt.xlabel('Saat')
plt.ylabel('Gün')

# Pik vaxtları işarələyək
plt.tight_layout()
plt.show()

# Kateqoriya və endirim səviyyəsi üzrə satışlar
cat_discount_sales = df.pivot_table(index='product_category', columns='discount_pct',
                                    values='quantity', aggfunc='sum', fill_value=0)

plt.figure(figsize=(12, 8))
sns.heatmap(cat_discount_sales, cmap='Reds', annot=True, fmt='g', linewidths=.5)
plt.title('Məhsul Kateqoriyası və Endirim Səviyyəsi üzrə Satış Sayı', fontsize=14)
plt.xlabel('Endirim Dərəcəsi')
plt.ylabel('Məhsul Kateqoriyası')
plt.tight_layout()
plt.show()

# Hər məhsul üçün orta qiymət və satış miqdarı
product_price_qty = df.groupby('product_name').agg({
    'final_price': 'mean',
    'quantity': 'sum'
}).reset_index()

plt.figure(figsize=(12, 8))
plt.scatter(product_price_qty['final_price'], product_price_qty['quantity'],
            alpha=0.7, s=100, c=product_price_qty['final_price'], cmap='viridis')

plt.title('Məhsul Qiyməti və Satış Miqdarı Arasındakı Əlaqə', fontsize=14)
plt.xlabel('Orta Qiymət')
plt.ylabel('Satış Miqdarı')
plt.colorbar(label='Qiymət')
plt.grid(True, alpha=0.3)

# Yüksək qiymətli və yüksək satış həcmli məhsulları işarələyək
for i, row in product_price_qty.iterrows():
    if row['quantity'] > 100 and row['final_price'] > 500:
        plt.annotate(row['product_name'],
                    (row['final_price'], row['quantity']),
                    xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.show()

# Kateqoriyalara görə Satış Qiymətlərinin Paylanması
plt.figure(figsize=(12, 8))
sns.boxplot(x='product_category', y='final_price', data=df, palette='Set3')
plt.title('Kateqoriyalara görə Qiymət Paylanması', fontsize=14)
plt.xlabel('Məhsul Kateqoriyası')
plt.ylabel('Qiymət')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Hər məhsul üçün orta qiymət və satış miqdarı
product_price_qty = df.groupby('product_name').agg({
    'final_price': 'mean',
    'quantity': 'sum'
}).reset_index()

# Yüksək qiymətli və/ya yüksək miqdarlı məhsulları seçək
high_price_threshold = product_price_qty['final_price'].quantile(0.85)
high_qty_threshold = product_price_qty['quantity'].quantile(0.75)

# # Önəmli məhsulları seçək
important_products = product_price_qty[
    (product_price_qty['final_price'] > high_price_threshold) | 
    ((product_price_qty['quantity'] > high_qty_threshold) & 
     (product_price_qty['final_price'] > product_price_qty['final_price'].median()))
].copy()

# Maksimum 8 məhsulu saxlayaq
if len(important_products) > 8:
    important_products = important_products.sort_values(
        ['final_price', 'quantity'], ascending=[False, False]
    ).head(8)

# Digər məhsulları ayrıca saxlayaq
other_products = product_price_qty[~product_price_qty['product_name'].isin(important_products['product_name'])]

# Qrafik yaradaq
plt.figure(figsize=(14, 10))

# İlk öncə digər məhsulları çəkək (background)
plt.scatter(other_products['final_price'], other_products['quantity'],
           alpha=0.5, s=70, c='lightgray', label='Digər məhsullar')

# Rəng paleti yaradaq
colors = plt.cm.tab10(np.linspace(0, 1, len(important_products)))

# Önəmli məhsulları fərqli rənglərlə çəkək
for i, (idx, row) in enumerate(important_products.iterrows()):
    plt.scatter(row['final_price'], row['quantity'],
               alpha=1.0, s=120, c=[colors[i]], 
               edgecolors='white', linewidths=1,
               label=row['product_name'])

plt.title('Məhsul Qiyməti və Satış Miqdarı Arasındakı Əlaqə', fontsize=18)
plt.xlabel('Orta Qiymət', fontsize=14)
plt.ylabel('Satış Miqdarı', fontsize=14)
plt.grid(True, alpha=0.3)

# X oxunu logarifmik miqyasda göstərək
plt.xscale('log')

# Leqendanı sağ tərəfdə və yuxarıda yerləşdirək
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), 
          fontsize=11, title='Məhsullar', title_fontsize=13,
          framealpha=0.8, edgecolor='gray')

# Əlavə yaxşılaşdırmalar
plt.gca().set_facecolor('#f8f9fa')
plt.grid(which='both', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
















