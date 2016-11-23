require 'rspec/support'
require 'rspec/core/formatters'

# module
module Spec
  module Helper
    # class
    class AlertingFormatter
      RSpec::Core::Formatters.register self, :example_started, :example_passed, :example_failed, :example_pending, :dump_summary

      def initialize(output)
        @output = output
        @started = 0
        @failed = 0
        @pending = 0
        @passed = 0
        @failures = []
      end

      def example_failed(notification)
        fd = truncate(notification.example.full_description.to_s, 130)
        l  = notification.example.example_group.location
        @failures << "#{l} - #{fd}"
        @failed += 1
      end

      def example_pending(_notification)
        @pending += 1
      end

      def example_passed(_notification)
        @passed += 1
      end

      def example_started(_notification)
        @started += 1
      end

      def dump_summary(_notification)
        @output << "[#{@failed}/#{@started}]"
        @output << " #{@failed} of #{@started} examples has failed"
        @output << ", #{@pending} examples pending" if @pending > 0
        @output << "\n"
        @output << @failures.join("\n")
        @output << "\n"
      end

      def truncate(what, length)
        return what if length > what.length
        "#{what[0..length]}..."
      end
    end
  end
end
