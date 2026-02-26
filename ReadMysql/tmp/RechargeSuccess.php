<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Carbon\Carbon;

/**
 * 充值成功记录模型
 *
 * @property int $cz_id 充值记录ID
 * @property string $cz_ddh 充值订单号
 * @property int $cz_lb 充值礼包类型
 * @property int $zeng_dian 赠送点数
 * @property int $extra_give_zd 额外赠送主点
 * @property int $extra_give_xd 额外赠送下点
 * @property int $coupon_give_zd 优惠券赠送点数
 * @property int $coupon_id 优惠券ID
 * @property int $lb_ye 礼包余额
 * @property int $zengdian_ye 赠点余额
 * @property int $package_vip_month 套餐会员月数
 * @property int $give_xr_time 赠送效果图时长
 * @property int $give_xr_vip_month 赠送效果图会员月数
 * @property int $give_zixue_vip_month 赠送自学会员月数
 * @property int $give_vr_vip_month 赠送VR会员月数
 * @property int $user_id 用户ID
 * @property int $cz_time 充值时间（Unix时间戳）
 * @property int $cz_source 充值来源
 * @property int $cz_type 充值类型
 * @property int $is_first 是否首充
 * @property int $is_all_first 是否全局首充
 * @property string $buyer_email 买家邮箱
 * @property float $total_fee 充值金额
 * @property int $activity_id 活动ID
 * @property int $package_choice 套餐选择
 * @property string $trade_no 交易流水号
 * @property string $pay_account 支付账号
 * @property int $package_vip_unit 套餐会员单位
 * @property int $give_xr_vip_unit 赠送效果图会员单位
 * @property int $give_animation_coin 赠送动画币
 * @property int $give_zixue_vip_unit 赠送自学会员单位
 * @property int $give_vr_vip_unit 赠送VR会员单位
 * @property int $give_res_vip_month 赠送资源会员月数
 * @property int $give_res_vip_unit 赠送资源会员单位
 * @property int $give_cloud_vip_month 赠送云会员月数
 * @property int $give_cloud_vip_unit 赠送云会员单位
 * @property int $give_cloud_super_vip_month 赠送云超级会员月数
 * @property int $give_cloud_super_vip_unit 赠送云超级会员单位
 * @property string $give_coupon_list 赠送优惠券列表
 * @property float $package_fee 套餐费用
 * @property int $give_base_res_vip_month 赠送基础资源会员月数
 * @property int $give_base_res_vip_unit 赠送基础资源会员单位
 */
class RechargeSuccess extends Model
{
    /**
     * 表名
     */
    protected $table = 'll_recharge_success';

    /**
     * 主键
     */
    protected $primaryKey = 'cz_id';

    /**
     * 数据库连接名
     */
    protected $connection = 'mysql';

    /**
     * 关闭自动维护时间戳
     * 因为表使用 cz_time 字段存储时间
     */
    public $timestamps = false;

    /**
     * 可批量赋值的属性
     */
    protected $fillable = [
        'cz_ddh',
        'cz_lb',
        'zeng_dian',
        'extra_give_zd',
        'extra_give_xd',
        'coupon_give_zd',
        'coupon_id',
        'lb_ye',
        'zengdian_ye',
        'package_vip_month',
        'give_xr_time',
        'give_xr_vip_month',
        'give_zixue_vip_month',
        'give_vr_vip_month',
        'user_id',
        'cz_time',
        'cz_source',
        'cz_type',
        'is_first',
        'is_all_first',
        'buyer_email',
        'total_fee',
        'activity_id',
        'package_choice',
        'trade_no',
        'pay_account',
        'package_vip_unit',
        'give_xr_vip_unit',
        'give_animation_coin',
        'give_zixue_vip_unit',
        'give_vr_vip_unit',
        'give_res_vip_month',
        'give_res_vip_unit',
        'give_cloud_vip_month',
        'give_cloud_vip_unit',
        'give_cloud_super_vip_month',
        'give_cloud_super_vip_unit',
        'give_coupon_list',
        'package_fee',
        'give_base_res_vip_month',
        'give_base_res_vip_unit',
    ];

    /**
     * 属性类型转换
     */
    protected $casts = [
        'cz_id' => 'integer',
        'cz_lb' => 'integer',
        'zeng_dian' => 'integer',
        'extra_give_zd' => 'integer',
        'extra_give_xd' => 'integer',
        'coupon_give_zd' => 'integer',
        'coupon_id' => 'integer',
        'lb_ye' => 'integer',
        'zengdian_ye' => 'integer',
        'package_vip_month' => 'integer',
        'give_xr_time' => 'integer',
        'give_xr_vip_month' => 'integer',
        'give_zixue_vip_month' => 'integer',
        'give_vr_vip_month' => 'integer',
        'user_id' => 'integer',
        'cz_time' => 'integer',
        'cz_source' => 'integer',
        'cz_type' => 'integer',
        'is_first' => 'boolean',
        'is_all_first' => 'boolean',
        'total_fee' => 'decimal:2',
        'activity_id' => 'integer',
        'package_choice' => 'integer',
        'package_vip_unit' => 'integer',
        'give_xr_vip_unit' => 'integer',
        'give_animation_coin' => 'integer',
        'give_zixue_vip_unit' => 'integer',
        'give_vr_vip_unit' => 'integer',
        'give_res_vip_month' => 'integer',
        'give_res_vip_unit' => 'integer',
        'give_cloud_vip_month' => 'integer',
        'give_cloud_vip_unit' => 'integer',
        'give_cloud_super_vip_month' => 'integer',
        'give_cloud_super_vip_unit' => 'integer',
        'package_fee' => 'decimal:2',
        'give_base_res_vip_month' => 'integer',
        'give_base_res_vip_unit' => 'integer',
    ];

    // ==================== 常量定义 ====================

    /**
     * 充值类型
     */
    const TYPE_NORMAL = 0;      // 普通充值
    const TYPE_PACKAGE = 1;     // 套餐充值
    const TYPE_ACTIVITY = 8;    // 活动充值
    const TYPE_SPECIAL = 9;     // 特殊充值

    /**
     * 充值来源
     */
    const SOURCE_WEB = 0;       // 网站
    const SOURCE_MOBILE = 3;    // 移动端
    const SOURCE_WECHAT = 8;    // 微信

    /**
     * 会员时间单位
     */
    const UNIT_DAY = 1;         // 天
    const UNIT_MONTH = 2;       // 月
    const UNIT_YEAR = 3;        // 年

    // ==================== 访问器 ====================

    /**
     * 充值时间的 Carbon 对象
     */
    protected function czDatetime(): Attribute
    {
        return Attribute::make(
            get: fn () => Carbon::createFromTimestamp($this->cz_time)
        );
    }

    /**
     * 是否大额充值（>=1000元）
     */
    protected function isLargeRecharge(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->total_fee >= 1000
        );
    }

    /**
     * 充值类型名称
     */
    protected function czTypeName(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->getTypeName($this->cz_type)
        );
    }

    /**
     * 充值来源名称
     */
    protected function czSourceName(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->getSourceName($this->cz_source)
        );
    }

    /**
     * 总赠送点数
     */
    protected function totalGivePoints(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->zeng_dian + $this->extra_give_zd + $this->coupon_give_zd
        );
    }

    /**
     * 会员赠送汇总
     */
    protected function vipSummary(): Attribute
    {
        return Attribute::make(
            get: fn () => [
                'package_vip' => $this->formatVipTime($this->package_vip_month, $this->package_vip_unit),
                'xr_vip' => $this->formatVipTime($this->give_xr_vip_month, $this->give_xr_vip_unit),
                'zixue_vip' => $this->formatVipTime($this->give_zixue_vip_month, $this->give_zixue_vip_unit),
                'vr_vip' => $this->formatVipTime($this->give_vr_vip_month, $this->give_vr_vip_unit),
                'res_vip' => $this->formatVipTime($this->give_res_vip_month, $this->give_res_vip_unit),
                'cloud_vip' => $this->formatVipTime($this->give_cloud_vip_month, $this->give_cloud_vip_unit),
                'cloud_super_vip' => $this->formatVipTime($this->give_cloud_super_vip_month, $this->give_cloud_super_vip_unit),
            ]
        );
    }

    /**
     * 是否有会员赠送
     */
    protected function hasVipGive(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->package_vip_month > 0
                || $this->give_xr_vip_month > 0
                || $this->give_zixue_vip_month > 0
                || $this->give_vr_vip_month > 0
                || $this->give_res_vip_month > 0
                || $this->give_cloud_vip_month > 0
                || $this->give_cloud_super_vip_month > 0
        );
    }

    // ==================== 查询作用域 ====================

    /**
     * 今日充值
     */
    public function scopeToday($query)
    {
        $todayStart = Carbon::today()->timestamp;
        return $query->where('cz_time', '>=', $todayStart);
    }

    /**
     * 最近N天
     */
    public function scopeRecent($query, $days = 7)
    {
        $cutoffTime = Carbon::now()->subDays($days)->timestamp;
        return $query->where('cz_time', '>=', $cutoffTime);
    }

    /**
     * 日期范围
     */
    public function scopeDateRange($query, $startDate, $endDate)
    {
        $startTimestamp = Carbon::parse($startDate)->timestamp;
        $endTimestamp = Carbon::parse($endDate)->timestamp;
        return $query->whereBetween('cz_time', [$startTimestamp, $endTimestamp]);
    }

    /**
     * 指定用户
     */
    public function scopeOfUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    /**
     * 大额充值
     */
    public function scopeLargeAmount($query, $minAmount = 1000)
    {
        return $query->where('total_fee', '>=', $minAmount);
    }

    /**
     * 首充用户
     */
    public function scopeFirstRecharge($query)
    {
        return $query->where('is_first', 1);
    }

    /**
     * 全局首充
     */
    public function scopeAllFirstRecharge($query)
    {
        return $query->where('is_all_first', 1);
    }

    /**
     * 按充值类型
     */
    public function scopeOfType($query, $type)
    {
        return $query->where('cz_type', $type);
    }

    /**
     * 按充值来源
     */
    public function scopeOfSource($query, $source)
    {
        return $query->where('cz_source', $source);
    }

    /**
     * 有活动
     */
    public function scopeHasActivity($query)
    {
        return $query->where('activity_id', '>', 0);
    }

    // ==================== 辅助方法 ====================

    /**
     * 获取充值类型名称
     */
    public static function getTypeName($type)
    {
        $types = [
            self::TYPE_NORMAL => '普通充值',
            self::TYPE_PACKAGE => '套餐充值',
            self::TYPE_ACTIVITY => '活动充值',
            self::TYPE_SPECIAL => '特殊充值',
        ];
        return $types[$type] ?? '未知类型';
    }

    /**
     * 获取充值来源名称
     */
    public static function getSourceName($source)
    {
        $sources = [
            self::SOURCE_WEB => '网站',
            self::SOURCE_MOBILE => '移动端',
            self::SOURCE_WECHAT => '微信',
        ];
        return $sources[$source] ?? '其他来源';
    }

    /**
     * 获取单位名称
     */
    public static function getUnitName($unit)
    {
        $units = [
            self::UNIT_DAY => '天',
            self::UNIT_MONTH => '月',
            self::UNIT_YEAR => '年',
        ];
        return $units[$unit] ?? '未知';
    }

    /**
     * 格式化会员时长
     */
    protected function formatVipTime($duration, $unit)
    {
        if ($duration <= 0) {
            return '无';
        }
        return $duration . self::getUnitName($unit);
    }

    /**
     * 转换为数组（用于API返回）
     */
    public function toArray()
    {
        $array = parent::toArray();

        // 添加计算属性
        $array['cz_datetime'] = $this->cz_datetime->format('Y-m-d H:M:S');
        $array['is_large_recharge'] = $this->is_large_recharge;
        $array['cz_type_name'] = $this->cz_type_name;
        $array['cz_source_name'] = $this->cz_source_name;
        $array['total_give_points'] = $this->total_give_points;
        $array['has_vip_give'] = $this->has_vip_give;

        return $array;
    }

    // ==================== 静态查询方法 ====================

    /**
     * 获取总体统计
     */
    public static function getTotalStats()
    {
        return self::selectRaw('
            COUNT(*) as total_count,
            SUM(total_fee) as total_amount,
            AVG(total_fee) as avg_amount,
            MAX(total_fee) as max_amount,
            MIN(total_fee) as min_amount
        ')->first();
    }

    /**
     * 按类型统计
     */
    public static function getStatsByType()
    {
        return self::selectRaw('
            cz_type,
            COUNT(*) as count,
            SUM(total_fee) as total_amount,
            AVG(total_fee) as avg_amount
        ')
        ->groupBy('cz_type')
        ->orderByDesc('count')
        ->get();
    }

    /**
     * 按来源统计
     */
    public static function getStatsBySource()
    {
        return self::selectRaw('
            cz_source,
            COUNT(*) as count,
            SUM(total_fee) as total_amount,
            AVG(total_fee) as avg_amount
        ')
        ->groupBy('cz_source')
        ->orderByDesc('count')
        ->get();
    }

    /**
     * 每日统计
     */
    public static function getDailyStats($days = 30)
    {
        $cutoffTime = Carbon::now()->subDays($days)->timestamp;

        return self::selectRaw('
            DATE(FROM_UNIXTIME(cz_time)) as date,
            COUNT(*) as count,
            SUM(total_fee) as total_amount
        ')
        ->where('cz_time', '>=', $cutoffTime)
        ->groupBy('date')
        ->orderByDesc('date')
        ->get();
    }

    /**
     * Top充值用户
     */
    public static function getTopUsers($limit = 100)
    {
        return self::selectRaw('
            user_id,
            COUNT(*) as recharge_count,
            SUM(total_fee) as total_amount
        ')
        ->groupBy('user_id')
        ->orderByDesc('total_amount')
        ->limit($limit)
        ->get();
    }
}
